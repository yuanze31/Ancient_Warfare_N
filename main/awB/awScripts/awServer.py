# -*- coding: utf-8 -*-

import random

import mod.server.extraServerApi as serverApi

compFactory = serverApi.GetEngineCompFactory()
ServerSystem = serverApi.GetServerSystemCls()


class awServerSystem(ServerSystem):

    def __init__(self, namespace, system_name):
        ServerSystem.__init__(self, namespace, system_name)
        self.namespace = serverApi.GetEngineNamespace()
        self.system_name = serverApi.GetEngineSystemName()

        self.ListenEvent()
        self.allow_spawn = 0
        print "awdebug:已启动Server"

    def ListenEvent(self):
        self.ListenForEvent(self.namespace, self.system_name, "ServerChatEvent", self, self.onServerChat)
        self.ListenForEvent(self.namespace, self.system_name, "ServerSpawnMobEvent", self, self.onServerSpawnMob)

    def UnListenEvent(self):
        self.UnListenForEvent(self.namespace, self.system_name, "ServerChatEvent", self, self.onServerChat)
        self.UnListenForEvent(self.namespace, self.system_name, "ServerSpawnMobEvent", self, self.onServerSpawnMob)

    def Destroy(self):
        self.UnListenEvent()

    def onServerChat(self, args):
        print "awdebug:收到消息！"
        if args["message"] == "awe":
            self.allow_spawn = 1
            print "awdebug:允许生成", self.allow_spawn
        elif args["message"] == "awd":
            self.allow_spawn = 0
            print "awdebug:禁止生成", self.allow_spawn
        else:
            print "awdebug:无动作"

    def onServerSpawnMob(self, args):
        entityid = args["entityId"]
        identifier = args["identifier"]
        # realIdentifier = args["realIdentifier"]
        if identifier == "aw:spawn":
            print "awdebug:收到生成", "-identifier", identifier, "-entityid", entityid, "-allowspawn", self.allow_spawn
            x = args["x"]
            y = args["y"]
            z = args["z"]
            print "x", x, "y", y, "z", z
            # 生成实体
            if self.allow_spawn == 1:
                result = self.onAWspawnspawn(x, y, z)
                if result is not None:
                    print "awdebug:生成成功"
                else:
                    print "awdebug:生成失败"
            # 销毁aw:spawn实体
            if self.DestroyEntity(entityid):
                print "awdebug:Desory success"
            else:
                print "awdebug:Desory fail"
            pass

    def onAWspawnspawn(self, x, y, z):
        def notNone(args):
            if args is None:
                return 0
            else:
                return 1

        def spawnBandit():
            result1 = self.CreateEngineEntityByTypeStr("aw:bandit_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
            result2 = self.CreateEngineEntityByTypeStr("aw:bandit_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
            result3 = self.CreateEngineEntityByTypeStr("aw:bandit_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
            result4 = self.CreateEngineEntityByTypeStr("aw:bandit_soldier_horse", (x, y + 1, z), (0, 0), 0)
            result5 = self.CreateEngineEntityByTypeStr("aw:bandit_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
            result6 = self.CreateEngineEntityByTypeStr("aw:bandit_general_horse", (x + 1, y + 1, z), (0, 0), 0)
            print result1, result2, result3, result4, result5, result6
            return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        def spawnDesert():
            result1 = self.CreateEngineEntityByTypeStr("aw:desert_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
            result2 = self.CreateEngineEntityByTypeStr("aw:desert_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
            result3 = self.CreateEngineEntityByTypeStr("aw:desert_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
            result4 = self.CreateEngineEntityByTypeStr("aw:desert_soldier_horse", (x, y + 1, z), (0, 0), 0)
            result5 = self.CreateEngineEntityByTypeStr("aw:desert_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
            result6 = self.CreateEngineEntityByTypeStr("aw:desert_general_horse", (x + 1, y + 1, z), (0, 0), 0)
            print result1, result2, result3, result4, result5, result6
            return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        def spawnNative():
            result1 = self.CreateEngineEntityByTypeStr("aw:native_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
            result2 = self.CreateEngineEntityByTypeStr("aw:native_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
            result3 = self.CreateEngineEntityByTypeStr("aw:native_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
            result4 = self.CreateEngineEntityByTypeStr("aw:native_soldier_horse", (x, y + 1, z), (0, 0), 0)
            result5 = self.CreateEngineEntityByTypeStr("aw:native_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
            result6 = self.CreateEngineEntityByTypeStr("aw:native_general_horse", (x + 1, y + 1, z), (0, 0), 0)
            print result1, result2, result3, result4, result5, result6
            return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        def spawnPirate():
            result1 = self.CreateEngineEntityByTypeStr("aw:pirate_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
            result2 = self.CreateEngineEntityByTypeStr("aw:pirate_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
            result3 = self.CreateEngineEntityByTypeStr("aw:pirate_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
            result4 = self.CreateEngineEntityByTypeStr("aw:pirate_soldier_horse", (x, y + 1, z), (0, 0), 0)
            result5 = self.CreateEngineEntityByTypeStr("aw:pirate_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
            result6 = self.CreateEngineEntityByTypeStr("aw:pirate_general_horse", (x + 1, y + 1, z), (0, 0), 0)
            print result1, result2, result3, result4, result5, result6
            return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        def spawnPlayer():
            result1 = self.CreateEngineEntityByTypeStr("aw:player_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
            result2 = self.CreateEngineEntityByTypeStr("aw:player_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
            result3 = self.CreateEngineEntityByTypeStr("aw:player_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
            result4 = self.CreateEngineEntityByTypeStr("aw:player_soldier_horse", (x, y + 1, z), (0, 0), 0)
            result5 = self.CreateEngineEntityByTypeStr("aw:player_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
            result6 = self.CreateEngineEntityByTypeStr("aw:player_general_horse", (x + 1, y + 1, z), (0, 0), 0)
            print result1, result2, result3, result4, result5, result6
            return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        def spawnViking():
            result1 = self.CreateEngineEntityByTypeStr("aw:viking_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
            result2 = self.CreateEngineEntityByTypeStr("aw:viking_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
            result3 = self.CreateEngineEntityByTypeStr("aw:viking_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
            result4 = self.CreateEngineEntityByTypeStr("aw:viking_soldier_horse", (x, y + 1, z), (0, 0), 0)
            result5 = self.CreateEngineEntityByTypeStr("aw:viking_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
            result6 = self.CreateEngineEntityByTypeStr("aw:viking_general_horse", (x + 1, y + 1, z), (0, 0), 0)
            print result1, result2, result3, result4, result5, result6
            return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        spawn_func = [spawnBandit(), spawnDesert(), spawnNative(), spawnPirate(), spawnPlayer(), spawnViking()]
        return spawn_func[random.randint(0, 5)]
