# -*- coding: UTF-8 -*-
from mod.server.system.serverSystem import ServerSystem
import mod.server.extraServerApi as serverApi
import math
from mod.common.utils.mcmath import Vector3
compFactory = serverApi.GetEngineCompFactory()

class Main(ServerSystem):

    def __init__(self, namespace, system_name):
        ServerSystem.__init__(self, namespace, system_name)
        namespace, system = serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName()

        #监听自身
        self.ListenForEvent(namespace, system, 'ProjectileDoHitEffectEvent', self, self.ProjectileDoHit)#子弹击中时
        #监听client端
        self.ListenForEvent('wand', 'wandClient',"ice_spring", self, self.ice_spring)
        self.ListenForEvent('wand', 'wandClient',"slow_burn", self, self.slow_burn)
        self.ListenForEvent('wand', 'wandClient',"bullet", self, self.bullet)
        
    def ProjectileDoHit(self,data):
        pid = data["id"]
        Ecomp = compFactory.CreateEngineType(pid)
        if Ecomp.GetEngineTypeStr()=="zt:ice_b":
            pos = (data["x"],data["y"],data["z"])
            self.BroadcastToAllClient("bullet_hit", {"pos":pos,"type":"ice","targetId":data["targetId"]})
        elif Ecomp.GetEngineTypeStr()=="zt:fire_b":
            pos = (data["x"],data["y"],data["z"])
            self.BroadcastToAllClient("bullet_hit", {"pos":pos,"type":"fire"})
        
    def ice_spring(self,data):
        entities = self.sector_attack(data)
        if len(entities)>0:
            for ei in entities:
                effectComp = compFactory.CreateEffect(ei)
                effectComp.AddEffectToEntity("slowness", 3, 2, False)
        
    def slow_burn(self,data):
        entities = self.sector_attack(data)
        if len(entities)>0:
            for ei in entities:
                Ccomp = compFactory.CreateAttr(ei)
                Ccomp.SetEntityOnFire(2, 2)

    def bullet(self,data):
        playerId=data["playerId"]
        ProjectileComp = compFactory.CreateProjectile(serverApi.GetLevelId())
        if data["type"]=="ice":
            ProjectileComp.CreateProjectileEntity(playerId, "zt:ice_b", {})
        else:
            ProjectileComp.CreateProjectileEntity(playerId, "zt:fire_b", {})
        
    #获取扇形区域    
    def sector_attack(self,data):
        player_id = data["playerId"]
        entities = compFactory.CreateGame(player_id).GetEntitiesAround(player_id, 10,
            {'any_of': {'test': 'is_family','subject': 'other','operator': 'not','value': 'player'}})
        entities2 = []
        for entity in entities:
            attacker_foot_pos = compFactory.CreatePos(player_id).GetFootPos()
            victim_foot_pos = compFactory.CreatePos(entity).GetFootPos()
            delta = Vector3(victim_foot_pos) - Vector3(attacker_foot_pos)
            forward_vector = serverApi.GetDirFromRot(compFactory.CreateRot(player_id).GetRot())
            angle = math.degrees(math.acos(Vector3.Dot(delta.Normalized(), Vector3(forward_vector).Normalized())))
            if angle < 65.0 and delta.Length() <=25 :
                print"ghost成功"
                entities2.append(entity)
                compHurt = compFactory.CreateHurt(entity)
                compHurt.Hurt(4, serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, player_id, None, False)
                Actioncomp = compFactory.CreateAction(entity)
                #xx,yy,zz = delta
                #Actioncomp.SetMobKnockback(xx, zz, 1.0, 0,1.5)击退
        return entities2        
                
               