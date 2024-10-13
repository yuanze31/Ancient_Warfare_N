# -*- coding: utf-8 -*-


import mod.server.extraServerApi as serverApi

compFactory = serverApi.GetEngineCompFactory()
ServerSystem = serverApi.GetServerSystemCls()


class awServerSystem(ServerSystem):

    def __init__(self, namespace, system_name):
        ServerSystem.__init__(self, namespace, system_name)
        namespace = serverApi.GetEngineNamespace()
        system_name = serverApi.GetEngineSystemName()

        self.ListenEvent()
        # self.allow_spawn = 0

    # 监听函数，用于定义和监听函数。函数名称除了强调的其他都是自取的，这个函数也是。
    def ListenEvent(self):
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerChatEvent", self, self.OnServerChat)

    # 反监听函数，用于反监听事件，在代码中有创建注册就对应了销毁反注册是一个好的编程习惯，不要依赖引擎来做这些事。
    def UnListenEvent(self):
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerChatEvent", self, self.OnServerChat)

    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        # 调用上面的反监听函数来销毁
        self.UnListenEvent()

    def OnServerChat(self, args):
        # playerId = args["playerId"]
        print "收到消息"
        if args["message"] == "awe":
            # self.allow_spawn = 1
            print "允许"
        elif args['message'] == "awd":
            # self.allow_spawn = 0
            print "禁止"
        else:
            print "无动作"
