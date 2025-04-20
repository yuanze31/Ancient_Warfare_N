# -*- coding: utf-8 -*-
import random

from QuModLibs.Server import *
from univFunction import randomName

CF = serverApi.GetEngineCompFactory()

if CF.CreateExtraData(levelId).GetExtraData("allow_spawn") is None:
    CF.CreateExtraData(levelId).SetExtraData("allow_spawn", 0)
else:
    allow_spawn = CF.CreateExtraData(levelId).GetExtraData("allowspawn")
if CF.CreateExtraData(levelId).GetExtraData("camp_spawn") is None:
    CF.CreateExtraData(levelId).SetExtraData("camp_spawn", [1, 1, 1, 1, 1, 1])
else:
    camp_spawn = CF.CreateExtraData(levelId).GetExtraData("camp_spawn")

Modnamespace = ["aw"]
Modcamp = ["bandit", "desert", "native", "pirate", "player", "viking"]
ModcampCN = ["土匪", "沙漠", "王国", "海盗", "玩家", "纳维亚海盗"]
Modtype = ["archer", "archer_horse", "axeman", "axeman_pro", "general", "general_horse", "lance", "soldier", "soldier_horse"]
ModtypeCN = ["弓箭手", "游骑兵", "斧兵", "重斧兵", "首领", "铁骑", "矛兵", "士兵", "骑兵"]


def getConfig(config_key):
    levelId = serverApi.GetLevelId()
    allow_spawn = CF.CreateExtraData(levelId).GetExtraData("allow_spawn")
    camp_spawn = CF.CreateExtraData(levelId).GetExtraData("camp_spawn")
    if config_key == "allow_spawn":
        return allow_spawn
    elif config_key == "camp_spawn":
        return camp_spawn


def setConfig(config_key, config_value):
    levelId = serverApi.GetLevelId()
    CF.CreateExtraData(levelId).SetExtraData(str(config_key), config_value)


@Listen(Events.ServerChatEvent)
def CtrlConfig(args):
    def spawnConfig(msg):
        allow_spawn = getConfig("allow_spawn")
        camp_spawn = getConfig("camp_spawn")
        # print "allowspawn" + str(allow_spawn)
        # print "camp_spawn" + str(camp_spawn)
        if msg == "awe":
            allow_spawn = True
            setConfig("allow_spawn", allow_spawn)
        elif msg == "awd":
            allow_spawn = False
            setConfig("allow_spawn", allow_spawn)

        msg_word = msg.split()
        if len(msg_word) == 2:
            for i in range(len(Modcamp)):
                if Modcamp[i] == msg_word[0]:
                    if msg_word[1] == "on":
                        camp_spawn[i] = 1
                        setConfig("camp_spawn", camp_spawn)
                    elif msg_word[1] == "off":
                        camp_spawn[i] = 0
                        setConfig("camp_spawn", camp_spawn)

    def displayConfig(args):
        username = args["username"]
        playerId = args["playerId"]
        message = args["message"]
        sendmsg = ""
        if message == "awc":
            allow_spawn = getConfig("allow_spawn")
            if allow_spawn == 1:
                sendmsg += "允许全部生成\n"
            elif allow_spawn == 0:
                sendmsg += "禁止全部生成\n"
            else:
                sendmsg += "全部生成配置错误\n"
            sendmsg += "====================\n"
            camp_spawn = getConfig("camp_spawn")
            n = 0
            for n, camp_spawni in enumerate(camp_spawn):
                if camp_spawni == 1:
                    sendmsg += "允许" + ModcampCN[n] + "类型生成\n"
                elif camp_spawni == 0:
                    sendmsg += "禁止" + ModcampCN[n] + "类型生成\n"
                else:
                    sendmsg += ModcampCN[n] + "配置错误！\n"
            # print "awdebug:sendmsg = \n" + str(sendmsg)
            args["cancel"] = True
            CF.CreateMsg(playerId).NotifyOneMessage(playerId, sendmsg, "§f")

    spawnConfig(args["message"])
    displayConfig(args)


@Listen(Events.ServerSpawnMobEvent)
def OnAWSpawnSpawn(args):
    def isAWspawnSpawn(args):
        entityid = args["entityId"]
        identifier = args["identifier"]
        allow_spawn = getConfig("allow_spawn")
        if identifier == "aw:spawn":
            if allow_spawn:
                print "awdebug:收到生成aw:spawn"
                x = args["x"]
                y = args["y"]
                z = args["z"]
                # print "x", x, "y", y, "z", z
                # 生成实体
                onAWspawnSpawn(x, y, z)
                # 销毁aw:spawn实体
                DestroyEntity(entityid)

    def onAWspawnSpawn(x, y, z):
        def notNone(args):
            if args is None:
                return 0
            else:
                return 1

        def spawnBandit(camp_spawn):
            if camp_spawn[0] == 1:
                result1 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:bandit_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                result2 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:bandit_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                result3 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:bandit_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                result4 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:bandit_soldier_horse", (x, y + 1, z), (0, 0), 0)
                result5 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:bandit_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                result6 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:bandit_general_horse", (x + 1, y + 1, z), (0, 0), 0)
                # print result1, result2, result3, result4, result5, result6
                return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        def spawnDesert(camp_spawn):
            if camp_spawn[1] == 1:
                result1 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:desert_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                result2 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:desert_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                result3 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:desert_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                result4 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:desert_soldier_horse", (x, y + 1, z), (0, 0), 0)
                result5 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:desert_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                result6 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:desert_general_horse", (x + 1, y + 1, z), (0, 0), 0)
                # print result1, result2, result3, result4, result5, result6
                return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        def spawnNative(camp_spawn):
            if camp_spawn[2] == 1:
                result1 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:native_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                result2 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:native_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                result3 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:native_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                result4 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:native_soldier_horse", (x, y + 1, z), (0, 0), 0)
                result5 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:native_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                result6 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:native_general_horse", (x + 1, y + 1, z), (0, 0), 0)
                # print result1, result2, result3, result4, result5, result6
                return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        def spawnPirate(camp_spawn):
            if camp_spawn[3] == 1:
                result1 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:pirate_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                result2 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:pirate_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                result3 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:pirate_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                result4 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:pirate_soldier_horse", (x, y + 1, z), (0, 0), 0)
                result5 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:pirate_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                result6 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:pirate_general_horse", (x + 1, y + 1, z), (0, 0), 0)
                # print result1, result2, result3, result4, result5, result6
                return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        def spawnPlayer(camp_spawn):
            if camp_spawn[4] == 1:
                result1 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:player_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                result2 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:player_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                result3 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:player_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                result4 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:player_soldier_horse", (x, y + 1, z), (0, 0), 0)
                result5 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:player_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                result6 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:player_general_horse", (x + 1, y + 1, z), (0, 0), 0)
                # print result1, result2, result3, result4, result5, result6
                return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        def spawnViking(camp_spawn):
            if camp_spawn[5] == 1:
                result1 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:viking_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                result2 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:viking_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                result3 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:viking_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                result4 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:viking_soldier_horse", (x, y + 1, z), (0, 0), 0)
                result5 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:viking_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                result6 = serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:viking_general_horse", (x + 1, y + 1, z), (0, 0), 0)
                # print result1, result2, result3, result4, result5, result6
                return all(notNone(r) for r in [result1, result2, result3, result4, result5, result6])

        camp_spawn = getConfig("camp_spawn")
        spawn_func = [spawnBandit(camp_spawn), spawnDesert(camp_spawn), spawnNative(camp_spawn), spawnPirate(camp_spawn), spawnPlayer(camp_spawn), spawnViking(camp_spawn)]
        return spawn_func[random.randint(0, 5)]

    isAWspawnSpawn(args)


@Listen(Events.AddEntityServerEvent)
def PlayerSummonEntity(args):
    def renameAWsoldier(args):
        identifier = args["engineTypeStr"]
        entityId = args["id"]
        if CF.CreateName(entityId).GetName() is None:
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
                            if part1 in Modnamespace and part3 in Modcamp and part4 in Modtype:
                                print(identifier + " 匹配成功!")
                                CF.CreateName(entityId).SetName(randomName("male"))
                            else:
                                print(identifier + " 不匹配.")
                    else:
                        if part1 in Modnamespace and part2 in Modcamp and part3 in Modtype:
                            print(identifier + " 匹配成功!")
                            CF.CreateName(entityId).SetName(randomName("male"))
                        else:
                            print(identifier + " 不匹配.")

    renameAWsoldier(args)
