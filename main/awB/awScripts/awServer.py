# -*- coding: utf-8 -*-
from QuModLibs.Server import *

from univFunction import compare_versions, randomName, parseAWIdentifier, getCampIndex, getCampCN, buildAWIdentifier, AW_CAMPS, AW_CAMPS_CN

CF = serverApi.GetEngineCompFactory()


def getConfig(config_key, id=levelId):
    return CF.CreateExtraData(id).GetExtraData(config_key)


def setConfig(config_key, config_value, id=levelId):
    CF.CreateExtraData(id).SetExtraData(str(config_key), config_value)


@AllowCall
def cilentRequestConfig(playerId="*"):
    configDict = {
            "allow_spawn": getConfig("allow_spawn"),
            "camp_spawn": getConfig("camp_spawn"),
            "soldier_name": getConfig("soldier_name")
            }
    Call(playerId, "syncCilentConfigCache", configDict)
    # print "向客户端同步配置，playerId：" + str(playerId)
    return configDict


@AllowCall
def cilentConfigUISave(playerId, newConfigDict={}):
    playerPerms = CF.CreatePlayer(playerId).GetPlayerAbilities()
    if playerPerms["op"]:
        new_allow_spawn = newConfigDict["allow_spawn"]
        new_camp_spawn = newConfigDict["camp_spawn"]
        new_soldier_name = newConfigDict["soldier_name"]
        setConfig("allow_spawn", new_allow_spawn)
        setConfig("camp_spawn", new_camp_spawn)
        setConfig("soldier_name", new_soldier_name)
        cilentRequestConfig()


@AllowCall
def getLastLoginVersion(playerId, NowVersion):
    LastLoginVersion = getConfig("LastLoginVersion", id=playerId)
    setConfig("LastLoginVersion", NowVersion, playerId)
    print "玩家：" + playerId + " 当前版本：" + NowVersion + " 上次版本：" + str(LastLoginVersion)
    if LastLoginVersion is None:
        return True
    elif compare_versions(NowVersion, LastLoginVersion) == 1:
        return True
    return False


@Listen(Events.CustomCommandTriggerServerEvent)
def AWdebug(args):
    def autoEnv():
        FullGameRuleDict = {
                'option_info': {
                        'pvp': bool,  # 玩家间伤害
                        'show_coordinates': bool,  # 显示坐标
                        'fire_spreads': bool,  # 火焰蔓延
                        'tnt_explodes': bool,  # TNT爆炸
                        'mob_loot': bool,  # 生物战利品
                        'natural_regeneration': bool,  # 自然生命恢复
                        'respawn_block_explosion': bool,  # 重生方块爆炸
                        'respawn_radius': int,  # 重生半径，请注意范围,目前支持[0,128]
                        'tile_drops': bool,  # 方块掉落
                        'immediate_respawn': bool  # 立即重生
                        },
                'cheat_info': {
                        'enable': bool,  # 激活作弊
                        'always_day': bool,  # 终为白日
                        'mob_griefing': bool,  # 生物破坏
                        'keep_inventory': bool,  # 保留物品栏
                        'weather_cycle': bool,  # 天气更替
                        'mob_spawn': bool,  # 生物生成
                        'entities_drop_loot': bool,  # 实体掉落战利品
                        'daylight_cycle': bool,  # 开启昼夜更替
                        'command_blocks_enabled': bool,  # 启用命令方块
                        'random_tick_speed': int,  # 随机刻速度
                        }
                }
        ruleDict = {
                'cheat_info': {
                        'enable': True,
                        'always_day': True,
                        'keep_inventory': True,
                        'weather_cycle': False,
                        'mob_spawn': False,
                        }
                }
        CF.CreateTime(levelId).SetTimeOfDay(6000)
        CF.CreateCommand(levelId).SetCommand("/weather clear", args["origin"]["entityId"], False)
        if CF.CreateGame(levelId).SetGameRulesInfoServer(ruleDict):
            return "调试环境设置§a成功"
        else:
            return "调试环境设置§c失败"

    command = args["command"]
    if command == "awdebug":
        if args["origin"]["entityId"] == "-4294967295":
            if args["args"][0]["value"] == "":
                args["return_msg_key"] = autoEnv()
            elif args["args"][0]["value"] == "ui":
                playerId = args["origin"]["entityId"]
                Call(playerId, "createConfigUI")
                args["return_msg_key"] = None
            elif args["args"][0]["value"] == "whatsnews":
                setConfig("LastLoginVersion", "1.0.0", "-4294967295")
        else:
            args["return_msg_key"] = None


@Listen(Events.CustomCommandTriggerServerEvent)
def EntityConfig(args):
    """
    古代战争生物生成设置
    """

    def Commandawspawn(variant, args):
        if variant == 0:
            allow_spawn = args[0]["value"]
            setConfig("allow_spawn", allow_spawn)
            return "所有阵营" + (" §a允许 §r生成" if allow_spawn else " §c禁止 §r生成")
        elif variant == 1:
            troop, allow = [item['value'] for item in args]
            camp_spawn = getConfig("camp_spawn")
            idx = getCampIndex(troop)
            if idx is not None:
                camp_spawn[idx] = allow
                setConfig("camp_spawn", camp_spawn)
                return getCampCN(troop) + "阵营" + (" §a允许 §r生成" if allow else " §c禁止 §r生成")

        return "§4未知错误 错误代码:awspawn"

    command = args["command"]
    if command == "awspawn":
        args["return_msg_key"] = Commandawspawn(args["variant"], args["args"])
        cilentRequestConfig()


@Listen(Events.CustomCommandTriggerServerEvent)
def NameConfig(args):
    command = args["command"]
    if command == "awname":
        soldier_name = args["args"][0]["value"]
        setConfig("soldier_name", soldier_name)
        if soldier_name == "male":
            args["return_msg_key"] = "手动放置士兵姓名设置：§9男性"
        elif soldier_name == "female":
            args["return_msg_key"] = "手动放置士兵姓名设置：§d女性"
        elif soldier_name == "off":
            args["return_msg_key"] = "手动放置士兵姓名设置：§c禁用"
        else:
            args["return_msg_key"] = "手动放置士兵姓名设置：§4错误"
        cilentRequestConfig()


@Listen(Events.CustomCommandTriggerServerEvent)
def DispConfig(args):
    def DispEntityConfig():
        allow_spawn = getConfig("allow_spawn")
        camp_spawn_config = getConfig("camp_spawn")

        if allow_spawn:
            all_spawn = "§r" + "所有阵营 §a允许 §r生成\n"
        elif not allow_spawn:
            all_spawn = "§r" + "所有阵营 §c禁止 §r生成\n"
        else:
            all_spawn = "§4" + "所有阵营 配置 错误\n"

        camp_spawn = ""
        for i in range(len(camp_spawn_config)):
            if camp_spawn_config[i]:
                camp_spawn += "§r" + AW_CAMPS_CN[i] + "阵营 §a允许 §r生成\n"
            elif not camp_spawn_config[i]:
                camp_spawn += "§r" + AW_CAMPS_CN[i] + "阵营 §c禁止 §r生成\n"
            else:
                camp_spawn += "§4" + AW_CAMPS_CN[i] + "阵营 配置 错误\n"

        return "§l=古代战争生物设置=\n" + "§r===================\n" + all_spawn + "§r-------------------\n" + camp_spawn

    def DispNameConfig():
        soldier_name = getConfig("soldier_name")
        if soldier_name == "male":
            return "手动放置士兵姓名设置：§9男性"
        elif soldier_name == "female":
            return "手动放置士兵姓名设置：§d女性"
        elif soldier_name == "off":
            return "手动放置士兵姓名设置：§c禁用"
        else:
            return "手动放置士兵姓名设置：§4错误"

    command = args["command"]
    if command == "awconfig":
        if args["args"][0]["value"] == "e" or args["args"][0]["value"] == "entity":
            args["return_msg_key"] = DispEntityConfig()
        elif args["args"][0]["value"] == "name":
            args["return_msg_key"] = DispNameConfig()
        elif args["args"][0]["value"] == "ui":
            playerId = args["origin"]["entityId"]
            Call(playerId, "createConfigUI")
            args["return_msg_key"] = None


@Listen(Events.ServerSpawnMobEvent)
def OnAWSpawnSpawn(args):
    def isAWspawnSpawn(args):
        entityid = args["entityId"]
        identifier = args["identifier"]
        if identifier == "aw:spawn":
            if getConfig("allow_spawn"):
                x = args["x"]
                y = args["y"]
                z = args["z"]
                # 生成实体
                onAWspawnSpawn(x, y, z)
                # 销毁aw:spawn实体
                DestroyEntity(entityid)

    def onAWspawnSpawn(x, y, z):
        camp_spawn = getConfig("camp_spawn")
        # 兵种与生成坐标偏移的映射
        spawn_types = [
                ("soldier", (x + 1, y + 1, z + 1)),
                ("soldier", (x + 1, y + 1, z - 1)),
                ("archer", (x - 1, y + 1, z - 1)),
                ("soldier_horse", (x, y + 1, z)),
                ("archer_horse", (x - 1, y + 1, z + 1)),
                ("general_horse", (x + 1, y + 1, z)),
                ]
        for i, camp in enumerate(AW_CAMPS):
            if camp_spawn[i] == 1:
                for etype, pos in spawn_types:
                    System.CreateEngineEntityByTypeStr(buildAWIdentifier(camp, etype), pos, (0, 0), 0)

    isAWspawnSpawn(args)


@Listen(Events.AddEntityServerEvent)
def PlayerSummonEntity(args):
    def renameAWsoldier(args):
        identifier = args["engineTypeStr"]
        if parseAWIdentifier(identifier):
            soldier_name = getConfig("soldier_name")
            if soldier_name != "off":
                entityId = args["id"]
                nameComp = CF.CreateName(entityId)
                if nameComp.GetName() is None:
                    nameComp.SetName(randomName(soldier_name))

    renameAWsoldier(args)


@Listen(Events.ProjectileDoHitEffectEvent)
def BombArrow(args):
    id = args["id"]
    pos = (args["x"], args["y"], args["z"])
    name = CF.CreateEngineType(id).GetEngineTypeStr()
    if name == "aw:bomb":
        CF.CreateExplosion(levelId).CreateExplosion(tuple(pos), 4, False, True, id, args["srcId"])


def DefaultConfig():
    """使用默认值初始化缺失的配置项"""
    default_config = {
            "allow_spawn": False,
            "camp_spawn": [True, True, True, True, True, True],
            "soldier_name": "male"
            }

    # 遍历所有默认配置项
    for key, value in default_config.items():
        if getConfig(key) is None:
            setConfig(key, value)


DefaultConfig()
