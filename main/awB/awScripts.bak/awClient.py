# -*- coding: utf-8 -*-

# 获取客户端引擎API模块
import mod.client.extraClientApi as clientApi

ClientSystem = clientApi.GetClientSystemCls()


# 在modMain中注册的Client System类
class awClientSystem(ClientSystem):

    def __init__(self, namespace, system_name):
        ClientSystem.__init__(self, namespace, system_name)
        namespace = clientApi.GetEngineNamespace()
        system_name = clientApi.GetEngineSystemName()

    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        pass
