from os import path

from aws_cdk import core
import aws_cdk.aws_lambda as lmb
import aws_cdk.aws_apigateway as apigw
import aws_cdk.aws_codedeploy as codedeploy
import aws_cdk.aws_cloudwatch as cloudwatch
import aws_cdk.aws_dynamodb as dynamodb

from utils import get_code

class PipelinesWebinarStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Dynamo table
        DYNAMO_TABLE_NAME = 'users'
        self.table = dynamodb.Table(self, 'dynamo_table', table_name=DYNAMO_TABLE_NAME,
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING)
        )
            # stream=dynamodb.StreamViewType.NEW_IMAGE

        # The code that defines your stack goes here
        # this_dir = path.dirname(__file__)

        self.get_users_fn = lmb.Function(self, 'GetUsers',
            runtime=lmb.Runtime.PYTHON_3_7,
            handler='index.handler',
            code=lmb.Code.inline(get_code('handler.py')),
            environment={
                'DYNAMOTABLE': self.table.table_name
            }
        )

        self.create_user_fn = lmb.Function(self, 'CreateUser',
            runtime=lmb.Runtime.PYTHON_3_7,
            handler='index.handler',
            code=lmb.Code.inline(get_code('create_user.py')),
            environment={
                'DYNAMOTABLE': self.table.table_name
            }
        )

        self.table.grant_read_write_data(self.get_users_fn)
        self.table.grant_read_write_data(self.create_user_fn)

        alias = lmb.Alias(self, 'HandlerAlias',
            alias_name='Current',
            version=self.get_users_fn.current_version)

        gw = apigw.RestApi(self, 'Gateway',
            description='Endpoint for a simple Lambda-powered web service')
        
        user_resource = gw.root.add_resource('users')
        user_resource.add_cors_preflight(
            allow_origins=apigw.Cors.ALL_ORIGINS,
            allow_methods=apigw.Cors.ALL_METHODS
        )
        get_users_api = apigw.LambdaIntegration(self.get_users_fn)
        user_resource.add_method('GET',  get_users_api)
        create_user_api = apigw.LambdaIntegration(self.create_user_fn)
        user_resource.add_method('POST', create_user_api)


        failure_alarm = cloudwatch.Alarm(self, 'FailureAlarm',
            metric=cloudwatch.Metric(
                metric_name='5XXError',
                namespace='AWS/ApiGateway',
                dimensions={
                    'ApiName': 'Gateway',
                },
                statistic='Sum',
                period=core.Duration.minutes(1)),
            threshold=1,
            evaluation_periods=1)

        codedeploy.LambdaDeploymentGroup(self, 'DeploymentGroup',
            alias=alias,
            deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE,
            alarms=[failure_alarm])

        self.url_output = core.CfnOutput(self, 'Url',
            value=gw.url)
