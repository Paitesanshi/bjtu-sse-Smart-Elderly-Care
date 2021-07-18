
"""
@file: recognition_request.py
@author: Looking
@email: 2392863668@qq.com
"""
 
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.asr.v20190614 import asr_client, models
import base64
try:
    cred = credential.Credential("AKIDLbglk656lKsDLNA6FBJDxb8XhuD1LcYn", "DOJkxzGm5S2oBerzPhAmuL1CKErCy2uW")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "asr.tencentcloudapi.com"
 
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = asr_client.AsrClient(cred, "ap-guangzhou", clientProfile)
 
    req = models.CreateRecTaskRequest()
    data=''
    with open('test.wav','rb') as f:
        wav_data=f.read()
        data=str(base64.b64encode(wav_data))
        print(type(wav_data))
    # 下面这个参数你自己根据需要进行设置
    data=data[1:-1]
    params = '{"EngineModelType":"16k_zh","ChannelNum":1,"ResTextFormat":0,"SourceType":1,"Data":"'+data+'"}'
    req.from_json_string(params)
    print(req)
    resp = client.CreateRecTask(req)
    print(resp.to_json_string())
 
except TencentCloudSDKException as err:
    print(err)