# -*- coding: utf-8 -*-

import random

import mod.server.extraServerApi as serverApi

from univFunction import randomName

compFactory = serverApi.GetEngineCompFactory()
ServerSystem = serverApi.GetServerSystemCls()


class awServerSystem(ServerSystem):

    def __init__(self, namespace, system_name):
        ServerSystem.__init__(self, namespace, system_name)
        self.namespace = serverApi.GetEngineNamespace()
        self.system_name = serverApi.GetEngineSystemName()

        levelId = serverApi.GetLevelId()

        if compFactory.CreateExtraData(levelId).GetExtraData("allow_spawn") is None:
            compFactory.CreateExtraData(levelId).SetExtraData("allow_spawn", 0)
        else:
            self.allow_spawn = compFactory.CreateExtraData(levelId).GetExtraData("allowspawn")
        if compFactory.CreateExtraData(levelId).GetExtraData("camp_spawn") is None:
            compFactory.CreateExtraData(levelId).SetExtraData("camp_spawn", [1, 1, 1, 1, 1, 1])
        else:
            self.camp_spawn = compFactory.CreateExtraData(levelId).GetExtraData("camp_spawn")

        self.Modnamespace = ["aw"]
        self.Modcamp = ["bandit", "desert", "native", "pirate", "player", "viking"]
        self.ModcampCN = ["土匪", "沙漠", "王国", "海盗", "玩家", "纳维亚海盗"]
        self.Modtype = ["archer", "archer_horse", "axeman", "axeman_pro", "general", "general_horse", "lance", "soldier", "soldier_horse"]
        self.ModtypeCN = ["弓箭手", "游骑兵", "斧兵", "重斧兵", "首领", "铁骑", "矛兵", "士兵", "骑兵"]

        self.ListenEvent()
        print "awdebug:已启动Server"

    def ListenEvent(self):
        self.ListenForEvent(self.namespace, self.system_name, "ServerChatEvent", self, self.onServerChat)
        self.ListenForEvent(self.namespace, self.system_name, "ServerSpawnMobEvent", self, self.onServerSpawnMob)
        self.ListenForEvent(self.namespace, self.system_name, "AddEntityServerEvent", self, self.onServerAddEntity)

    def UnListenEvent(self):
        self.UnListenForEvent(self.namespace, self.system_name, "ServerChatEvent", self, self.onServerChat)
        self.UnListenForEvent(self.namespace, self.system_name, "ServerSpawnMobEvent", self, self.onServerSpawnMob)
        self.UnListenForEvent(self.namespace, self.system_name, "AddEntityServerEvent", self, self.onServerAddEntity)

    def Destroy(self):
        self.UnListenEvent()

    def onServerChat(self, args):
        self.spawnConfig(args["message"])
        self.displayConfig(args)

    def onServerSpawnMob(self, args):
        self.isAWspawnSpawn(args)

    def onServerAddEntity(self, args):
        self.renameAWsoldier(args)

    # 判断是否是aw:spawn生成
    def isAWspawnSpawn(self, args):
        entityid = args["entityId"]
        identifier = args["identifier"]
        allow_spawn = self.getConfig("allow_spawn")
        if identifier == "aw:spawn":
            if allow_spawn == True:
                print "awdebug:收到生成aw:spawn"
                x = args["x"]
                y = args["y"]
                z = args["z"]
                # print "x", x, "y", y, "z", z
                # 生成实体
                self.onAWspawnSpawn(x, y, z)
                # 销毁aw:spawn实体
                self.DestroyEntity(entityid)

    # aw:spawn生成时，判断具体生成哪一阵营士兵
    def onAWspawnSpawn(self, x, y, z):
        def notNone(args):
            if args is None:
                return 0
            else:
                return 1

        def spawnBandit(camp_spawn):
            if camp_spawn[0] == 1:
                result1 = self.CreateEngineEntityByTypeStr("aw:bandit_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                result2 = self.CreateEngineEntityByTypeStr("aw:bandit_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                result3 = self.CreateEngineEntityByTypeStr("aw:bandit_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                result4 = self.CreateEngineEntityByTypeStr("aw:bandit_soldier_horse", (x, y + 1, z), (0, 0), 0)
                result5 = self.CreateEngineEntityByTypeStr("aw:bandit_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                result6 = self.CreateEngineEntityByTypeStr("aw:bandit_general_horse", (x + 1, y + 1, z), (0, 0), 0)
                # print result1, result2, result3, result4, result5, result6
                return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        def spawnDesert(camp_spawn):
            if camp_spawn[1] == 1:
                result1 = self.CreateEngineEntityByTypeStr("aw:desert_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                result2 = self.CreateEngineEntityByTypeStr("aw:desert_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                result3 = self.CreateEngineEntityByTypeStr("aw:desert_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                result4 = self.CreateEngineEntityByTypeStr("aw:desert_soldier_horse", (x, y + 1, z), (0, 0), 0)
                result5 = self.CreateEngineEntityByTypeStr("aw:desert_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                result6 = self.CreateEngineEntityByTypeStr("aw:desert_general_horse", (x + 1, y + 1, z), (0, 0), 0)
                # print result1, result2, result3, result4, result5, result6
                return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        def spawnNative(camp_spawn):
            if camp_spawn[2] == 1:
                result1 = self.CreateEngineEntityByTypeStr("aw:native_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                result2 = self.CreateEngineEntityByTypeStr("aw:native_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                result3 = self.CreateEngineEntityByTypeStr("aw:native_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                result4 = self.CreateEngineEntityByTypeStr("aw:native_soldier_horse", (x, y + 1, z), (0, 0), 0)
                result5 = self.CreateEngineEntityByTypeStr("aw:native_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                result6 = self.CreateEngineEntityByTypeStr("aw:native_general_horse", (x + 1, y + 1, z), (0, 0), 0)
                # print result1, result2, result3, result4, result5, result6
                return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        def spawnPirate(camp_spawn):
            if camp_spawn[3] == 1:
                result1 = self.CreateEngineEntityByTypeStr("aw:pirate_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                result2 = self.CreateEngineEntityByTypeStr("aw:pirate_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                result3 = self.CreateEngineEntityByTypeStr("aw:pirate_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                result4 = self.CreateEngineEntityByTypeStr("aw:pirate_soldier_horse", (x, y + 1, z), (0, 0), 0)
                result5 = self.CreateEngineEntityByTypeStr("aw:pirate_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                result6 = self.CreateEngineEntityByTypeStr("aw:pirate_general_horse", (x + 1, y + 1, z), (0, 0), 0)
                # print result1, result2, result3, result4, result5, result6
                return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        def spawnPlayer(camp_spawn):
            if camp_spawn[4] == 1:
                result1 = self.CreateEngineEntityByTypeStr("aw:player_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                result2 = self.CreateEngineEntityByTypeStr("aw:player_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                result3 = self.CreateEngineEntityByTypeStr("aw:player_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                result4 = self.CreateEngineEntityByTypeStr("aw:player_soldier_horse", (x, y + 1, z), (0, 0), 0)
                result5 = self.CreateEngineEntityByTypeStr("aw:player_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                result6 = self.CreateEngineEntityByTypeStr("aw:player_general_horse", (x + 1, y + 1, z), (0, 0), 0)
                # print result1, result2, result3, result4, result5, result6
                return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        def spawnViking(camp_spawn):
            if camp_spawn[5] == 1:
                result1 = self.CreateEngineEntityByTypeStr("aw:viking_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                result2 = self.CreateEngineEntityByTypeStr("aw:viking_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                result3 = self.CreateEngineEntityByTypeStr("aw:viking_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                result4 = self.CreateEngineEntityByTypeStr("aw:viking_soldier_horse", (x, y + 1, z), (0, 0), 0)
                result5 = self.CreateEngineEntityByTypeStr("aw:viking_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                result6 = self.CreateEngineEntityByTypeStr("aw:viking_general_horse", (x + 1, y + 1, z), (0, 0), 0)
                # print result1, result2, result3, result4, result5, result6
                return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        camp_spawn = self.getConfig("camp_spawn")
        spawn_func = [spawnBandit(camp_spawn), spawnDesert(camp_spawn), spawnNative(camp_spawn), spawnPirate(camp_spawn), spawnPlayer(camp_spawn), spawnViking(camp_spawn)]
        return spawn_func[random.randint(0, 5)]

    # 根据消息配置生成规则
    def spawnConfig(self, msg):
        allow_spawn = self.getConfig("allow_spawn")
        camp_spawn = self.getConfig("camp_spawn")
        # print "allowspawn" + str(allow_spawn)
        # print "camp_spawn" + str(camp_spawn)
        if msg == "awe":
            allow_spawn = True
            self.setConfig("allow_spawn", allow_spawn)
        elif msg == "awd":
            allow_spawn = False
            self.setConfig("allow_spawn", allow_spawn)

        msg_word = msg.split()
        if len(msg_word) == 2:
            for i in range(len(self.Modcamp)):
                if self.Modcamp[i] == msg_word[0]:
                    if msg_word[1] == "on":
                        camp_spawn[i] = 1
                        self.setConfig("camp_spawn", camp_spawn)
                    elif msg_word[1] == "off":
                        camp_spawn[i] = 0
                        self.setConfig("camp_spawn", camp_spawn)

    # 展示模组配置
    def displayConfig(self, args):
        username = args["username"]
        playerId = args["playerId"]
        message = args["message"]
        sendmsg = ""
        if message == "awc":
            allow_spawn = self.getConfig("allow_spawn")
            if allow_spawn == 1:
                sendmsg += "允许全部生成\n"
            elif allow_spawn == 0:
                sendmsg += "禁止全部生成\n"
            else:
                sendmsg += "全部生成配置错误\n"
            sendmsg += "====================\n"
            camp_spawn = self.getConfig("camp_spawn")
            n = 0
            for n, camp_spawni in enumerate(camp_spawn):
                if camp_spawni == 1:
                    sendmsg += "允许" + self.ModcampCN[n] + "类型生成\n"
                elif camp_spawni == 0:
                    sendmsg += "禁止" + self.ModcampCN[n] + "类型生成\n"
                else:
                    sendmsg += self.ModcampCN[n] + "配置错误！\n"
            # print "awdebug:sendmsg = \n" + str(sendmsg)
            args["cancel"] = True
            compFactory.CreateMsg(playerId).NotifyOneMessage(playerId, sendmsg, "§f")

    def getConfig(self, config_key):
        levelId = serverApi.GetLevelId()
        allow_spawn = compFactory.CreateExtraData(levelId).GetExtraData("allow_spawn")
        camp_spawn = compFactory.CreateExtraData(levelId).GetExtraData("camp_spawn")
        if config_key == "allow_spawn":
            return allow_spawn
        elif config_key == "camp_spawn":
            return camp_spawn

    def setConfig(self, config_key, config_value):
        levelId = serverApi.GetLevelId()
        compFactory.CreateExtraData(levelId).SetExtraData(str(config_key), config_value)

    def renameAWsoldier(self, args):
        identifier = args["engineTypeStr"]
        entityId = args["id"]
        if compFactory.CreateName(entityId).GetName() == None:
            # 切分命名空间
            parts = identifier.split(":")
            if len(parts) == 2:
                part1 = parts[0]

                # id判断
                part23 = parts[1].split("_", 1)
                if len(part23) == 2:
                    part2, part3 = part23
                    if part2 == "old":
                        part34 = part3.split("_", 1)
                        if len(part34) == 2:
                            part3, part4 = part34
                            if part1 in self.Modnamespace and part3 in self.Modcamp and part4 in self.Modtype:
                                print(identifier + " 匹配成功!")
                                compFactory.CreateName(entityId).SetName(randomName("male"))
                            else:
                                print(identifier + " 不匹配.")
                    else:
                        if part1 in self.Modnamespace and part2 in self.Modcamp and part3 in self.Modtype:
                            print(identifier + " 匹配成功!")
                            compFactory.CreateName(entityId).SetName(randomName("male"))
                        else:
                            print(identifier + " 不匹配.")
