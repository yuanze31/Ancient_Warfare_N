# -*- coding: utf-8 -*-
import math

from QuModLibs.Server import *

from univFunction import compare_versions, randomName, parseAWIdentifier, getCampIndex, getCampCN, buildAWIdentifier, AW_CAMPS, AW_CAMPS_CN

CF = serverApi.GetEngineCompFactory()


@Listen(Events.DamageEvent)
def hitShieldSoldier(args):
    AWIdentifier = parseAWIdentifier(CF.CreateEngineType(args["entityId"]).GetEngineTypeStr())
    if AWIdentifier and AWIdentifier["type"] == "soldier":
        if args["cause"] == "entity_attack":
            # 计算攻击方是否在范围内
            srcPos = CF.CreatePos(args["srcId"]).GetPos()
            tgtPos = CF.CreatePos(args["entityId"]).GetPos()
            tgtRot = CF.CreateRot(args["entityId"]).GetRot()
            dx, dy, dz = srcPos[0] - tgtPos[0], srcPos[1] - tgtPos[1], srcPos[2] - tgtPos[2]
            forward = serverApi.GetDirFromRot(tgtRot)
            h_dist = math.sqrt(dx * dx + dz * dz)
            f_h = math.sqrt(forward[0] * forward[0] + forward[2] * forward[2])
            if h_dist > 0.001 and f_h > 0.001:
                cos_yaw = (dx * forward[0] + dz * forward[2]) / (h_dist * f_h)
                in_range = cos_yaw >= 0.5 and abs(math.degrees(math.atan2(-dy, h_dist))) <= 70.0
            else:
                in_range = abs(math.degrees(math.atan2(-dy, h_dist))) <= 70.0

            if in_range:
                # 取消伤害
                args["damage"] = 0.0
                args["knock"] = False
                args["ignite"] = False
                # 生成特效
                Call("*", "showShieldSuccessEffect", CF.CreateDimension(args["entityId"]).GetEntityDimensionId(), CF.CreatePos(args["srcId"]).GetPos())
