from aws_cdk import core
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines
from aws_cdk import aws_iam as iam

from pipelines_webinar import constants

from .webservice_stage import WebServiceStage


APP_ACCOUNT = '475414269301'

class PipelineStack(core.Stack):
  def __init__(self, scope: core.Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    source_artifact = codepipeline.Artifact()
    cloud_assembly_artifact = codepipeline.Artifact()

    pipeline = pipelines.CdkPipeline(self, 'Pipeline',
      cloud_assembly_artifact=cloud_assembly_artifact,
    #   cross_account_keys=False, # no KMS no 1$ pay I'll have to pay so I'll comment sadge
      pipeline_name='WebinarPipeline',

      source_action=cpactions.GitHubSourceAction(
        action_name='GitHub',
        output=source_artifact,
        oauth_token=core.SecretValue.secrets_manager('github-token'),
        owner='DaviRolim',
        repo='cdk-pipelines-sample',
        branch='main',
        trigger=cpactions.GitHubTrigger.WEBHOOK),

      synth_action=pipelines.SimpleSynthAction(
        source_artifact=source_artifact,
        cloud_assembly_artifact=cloud_assembly_artifact,
        install_command='npm install -g aws-cdk && pip install -r requirements.txt',
        build_command='python -m unittest discover tests',
        synth_command='cdk synth'))

    pre_prod_app = WebServiceStage(self, 'Test', is_test=True, env={
      'account': APP_ACCOUNT,
      'region': 'us-east-2',
    })
    pre_prod_stage = pipeline.add_application_stage(pre_prod_app)
    pre_prod_stage.add_actions(pipelines.ShellScriptAction(
      action_name='IntegrationTest',
      run_order=pre_prod_stage.next_sequential_run_order(),
      additional_artifacts=[source_artifact],
      commands=[
        # 'pip install -r requirements.txt',
        'pip install pytest requests',
        'pytest integtests',
      ],
      use_outputs={
        'SERVICE_URL': pipeline.stack_output(pre_prod_app.url_output),
        'TABLE_NAME': pipeline.stack_output(pre_prod_app.table_name)
      }))
    prod_stage = pipeline.add_application_stage(WebServiceStage(self, 'Prod', is_test=False, env={
      'account': APP_ACCOUNT,
      'region': 'us-east-2',
    }))
    permission_delete_cf = iam.PolicyStatement(
      actions=['cloudformation:DeleteStack'],
      effect=iam.Effect.ALLOW,
      resources=['*']
    )
    prod_stage.add_actions(pipelines.ShellScriptAction(
      action_name='RemoveTestResources',
      additional_artifacts=[source_artifact],
      run_order=prod_stage.next_sequential_run_order(),
      commands=[
        f'aws cloudformation delete-stack --stack-name {constants.TEST_STACK_NAME}'
      ],
      role_policy_statements=[permission_delete_cf]
    ))


