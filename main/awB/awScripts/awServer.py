# -*- coding: utf-8 -*-
import random

from QuModLibs.Server import *

import modInfo
from univFunction import compare_versions, randomName

CF = serverApi.GetEngineCompFactory()

Modnamespace = ["aw"]
Modcamp = ["bandit", "desert", "native", "pirate", "player", "viking"]
ModcampCN = ["土匪", "沙漠", "帝国", "海盗", "新星", "纳维亚海盗"]
Modtype = ["archer", "archer_horse", "axeman", "axeman_pro", "general", "general_horse", "lance", "soldier", "soldier_horse"]
ModtypeCN = ["弓箭手", "游骑兵", "斧兵", "重斧兵", "首领", "铁骑", "矛兵", "战士", "骑兵"]

CONFIG_MAP = {
        "allow_spawn": "allow_spawn",
        "camp_spawn": "camp_spawn",
        "soldier_name": "soldier_name",
        "last_start_mod_version": "last_start_mod_version"
        }


def getConfig(config_key):
    level_id = serverApi.GetLevelId()
    # 根据映射表查找对应的ExtraData键名
    extra_data_key = CONFIG_MAP.get(config_key)
    return CF.CreateExtraData(level_id).GetExtraData(extra_data_key)


def setConfig(config_key, config_value):
    levelId = serverApi.GetLevelId()
    CF.CreateExtraData(levelId).SetExtraData(str(config_key), config_value)


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
        print args
        if args["origin"]["entityId"] == "-4294967295":
            if args["args"][0]["value"] == "":
                args["return_msg_key"] = autoEnv()
            elif args["args"][0]["value"] == "ui":
                playerId = args["origin"]["entityId"]
                Call(playerId, "createConfigUI")
                args["return_msg_key"] = None
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
            for i in range(len(Modcamp)):
                if Modcamp[i] == troop:
                    camp_spawn[i] = allow
                    setConfig("camp_spawn", camp_spawn)
                    return ModcampCN[i] + "阵营" + (" §a允许 §r生成" if allow else " §c禁止 §r生成")

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
                camp_spawn += "§r" + ModcampCN[i] + "阵营 §a允许 §r生成\n"
            elif not camp_spawn_config[i]:
                camp_spawn += "§r" + ModcampCN[i] + "阵营 §c禁止 §r生成\n"
            else:
                camp_spawn += "§4" + ModcampCN[i] + "阵营 配置 错误\n"

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
        def spawnBandit(camp_spawn):
            if camp_spawn[0] == 1:
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:bandit_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:bandit_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:bandit_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:bandit_soldier_horse", (x, y + 1, z), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:bandit_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:bandit_general_horse", (x + 1, y + 1, z), (0, 0), 0)

        def spawnDesert(camp_spawn):
            if camp_spawn[1] == 1:
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:desert_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:desert_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:desert_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:desert_soldier_horse", (x, y + 1, z), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:desert_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:desert_general_horse", (x + 1, y + 1, z), (0, 0), 0)

        def spawnNative(camp_spawn):
            if camp_spawn[2] == 1:
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:native_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:native_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:native_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:native_soldier_horse", (x, y + 1, z), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:native_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:native_general_horse", (x + 1, y + 1, z), (0, 0), 0)

        def spawnPirate(camp_spawn):
            if camp_spawn[3] == 1:
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:pirate_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:pirate_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:pirate_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:pirate_soldier_horse", (x, y + 1, z), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:pirate_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:pirate_general_horse", (x + 1, y + 1, z), (0, 0), 0)

        def spawnPlayer(camp_spawn):
            if camp_spawn[4] == 1:
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:player_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:player_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:player_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:player_soldier_horse", (x, y + 1, z), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:player_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:player_general_horse", (x + 1, y + 1, z), (0, 0), 0)

        def spawnViking(camp_spawn):
            if camp_spawn[5] == 1:
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:viking_soldier", (x + 1, y + 1, z + 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:viking_soldier", (x + 1, y + 1, z - 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:viking_archer", (x - 1, y + 1, z - 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:viking_soldier_horse", (x, y + 1, z), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:viking_archer_horse", (x - 1, y + 1, z + 1), (0, 0), 0)
                serverApi.GetServerSystemCls().CreateEngineEntityByTypeStr("aw:viking_general_horse", (x + 1, y + 1, z), (0, 0), 0)

        camp_spawn = getConfig("camp_spawn")
        spawn_func = [spawnBandit(camp_spawn), spawnDesert(camp_spawn), spawnNative(camp_spawn), spawnPirate(camp_spawn), spawnPlayer(camp_spawn), spawnViking(camp_spawn)]
        return spawn_func[random.randint(0, 5)]

    isAWspawnSpawn(args)


@Listen(Events.AddEntityServerEvent)
def PlayerSummonEntity(args):
    def renameAWsoldier(args):
        if getConfig("soldier_name") != "off":
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
                                    CF.CreateName(entityId).SetName(randomName(getConfig("soldier_name")))
                        else:
                            if part1 in Modnamespace and part2 in Modcamp and part3 in Modtype:
                                CF.CreateName(entityId).SetName(randomName(getConfig("soldier_name")))

    renameAWsoldier(args)


def popWhatsNewUI(versionNow, versionLast):
    print "当前版本：" + versionNow + "\n上次版本：" + versionLast + "\n弹出What\'s news弹窗（TODO）"
    # TODO: What's news 弹窗
    setConfig("last_start_mod_version", versionNow)


def DefaultConfig():
    """使用默认值初始化缺失的配置项"""
    default_config = {
            "allow_spawn": False,
            "camp_spawn": [True, True, True, True, True, True],
            "soldier_name": "male",
            "last_start_mod_version": "0.0.0"
            }

    # 遍历所有默认配置项
    for key, value in default_config.items():
        if getConfig(key) is None:
            setConfig(key, value)


DefaultConfig()
if compare_versions(modInfo.MOD_VERSION, getConfig("last_start_mod_version")) == 1:
    popWhatsNewUI(modInfo.MOD_VERSION, getConfig("last_start_mod_version"))
