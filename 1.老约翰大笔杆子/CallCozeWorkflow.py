"""
This example describes how to use the workflow interface to chat.
"""

import os
from typing import Optional

from cozepy import COZE_CN_BASE_URL, ChatStatus, Coze, DeviceOAuthApp, Message, MessageContentType, TokenAuth  # noqa
from settings import *
import asyncio

class CallCozeWorkflow:
    """
    大量借鉴了coze官方的workflow相关代码
    """
    def __init__(self,global_text_dict):
        self.global_text_dict = global_text_dict
        # Init the Coze client through the access_token.
        self.coze_client = Coze(auth=TokenAuth(token=self.get_coze_api_token()), base_url=self.get_coze_api_base())

    def get_coze_api_base(self) -> str:
        # The default access is api.coze.cn, but if you need to access api.coze.com,
        # please use base_url to configure the api endpoint to access
        coze_api_base = os.getenv("COZE_API_BASE")
        if coze_api_base:
            return coze_api_base

        return COZE_CN_BASE_URL  # default


    def get_coze_api_token(self,workspace_id: Optional[str] = None) -> str:
        # Get an access_token through personal access token or oauth.
        #coze_api_token = os.getenv("COZE_API_TOKEN")
        if coze_api_token:
            return coze_api_token

        coze_api_base = self.get_coze_api_base()

        device_oauth_app = DeviceOAuthApp(client_id="57294420732781205987760324720643.app.coze", base_url=coze_api_base)
        device_code = device_oauth_app.get_device_code(workspace_id)
        print(f"Please Open: {device_code.verification_url} to get the access token")
        return device_oauth_app.get_access_token(device_code=device_code.device_code, poll=True).access_token

    def callWFStructGen(self,):
        """
        调用大纲生成的workflow
        """
        shenfen=self.global_text_dict['shenfen']
        changhe=self.global_text_dict['changhe']
        leixing=self.global_text_dict['leixing']
        zhuti=self.global_text_dict['zhuti']
        # Create a workflow instance in Coze, copy the last number from the web link as the workflow's ID.
        workflow_id = coze_workflow_dice['大纲生成']
        # Call the coze.workflows.runs.create method to create a workflow run. The create method
        # is a non-streaming chat and will return a WorkflowRunResult class.
        workflow = self.coze_client.workflows.runs.create(
            workflow_id=workflow_id,
            parameters={"shenfen":shenfen,"changhe":changhe,"leixing":leixing,"zhuti":zhuti}
        )
        import json 
        res = json.loads(workflow.data)
        self.global_text_dict['title'] = res['output']
        self.global_text_dict['struct'] = res['output_struct']
        print(self.global_text_dict)
        self.global_text_dict['btn_enable'] = True
        #return (workflow.data['output'],workflow.data['output_struct'])
    def callContentGen(self):
        """
        调用文本生成的workflow
        """
        title=self.global_text_dict['title']
        text_struct=self.global_text_dict['struct']
        shenfen=self.global_text_dict['shenfen']
        changhe=self.global_text_dict['changhe']
        leixing=self.global_text_dict['leixing']
        zhuti=self.global_text_dict['zhuti']
        # Create a workflow instance in Coze, copy the last number from the web link as the workflow's ID.
        workflow_id = coze_workflow_dice['文本生成']
        # Call the coze.workflows.runs.create method to create a workflow run. The create method
        # is a non-streaming chat and will return a WorkflowRunResult class.
        workflow = self.coze_client.workflows.runs.create(
            workflow_id=workflow_id,
            parameters={"title":title,"text_struct":text_struct,"shenfen":shenfen,"changhe":changhe,"leixing":leixing,"zhuti":zhuti}
        )
        import json 
        res = json.loads(workflow.data)
        self.global_text_dict['content'] = res['data']
        print(self.global_text_dict)

if __name__ == '__main__':
    global_text_dict = {
        "shenfen":"总经理",
        "changhe":"年终总结发言",
        "leixing":"总结",
        "zhuti":"天马行空和一心一意",
        "title":"",
        "struct":"",
        "content":"",
        "btn_enable":True
    }
    obj = CallCozeWorkflow(global_text_dict)
    obj.callWFStructGen()
    obj.callContentGen()
    print(global_text_dict)