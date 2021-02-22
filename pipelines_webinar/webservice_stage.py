from aws_cdk import core

from .pipelines_webinar_stack import PipelinesWebinarStack

class WebServiceStage(core.Stage):
  def __init__(self, scope: core.Construct, id: str, env: str, **kwargs):
    super().__init__(scope, id, **kwargs)
    # core.Stage
    service = PipelinesWebinarStack(self, 'WebService', env)

    self.url_output = service.url_output
    self.table_name = service.table_name