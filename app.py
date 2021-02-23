#!/usr/bin/env python3

from aws_cdk import core

from pipelines_webinar.pipeline_stack import PipelineStack

from pipelines_webinar.pipelines_webinar_stack import PipelinesWebinarStack


app = core.App()
PipelineStack(app, "pipelines-webinar", delete_test_resources=True, env={'region': 'us-east-2'})

app.synth()
