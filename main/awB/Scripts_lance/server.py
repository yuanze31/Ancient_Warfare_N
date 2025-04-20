# -*- coding: UTF-8 -*-

import math

import mod.server.extraServerApi as serverApi
from mod.common.utils.mcmath import Vector3

compFactory = serverApi.GetEngineCompFactory()
ServerSystem = serverApi.GetServerSystemCls()


class AnimationServer(ServerSystem):

    def __init__(self, namespace, system_name):
        ServerSystem.__init__(self, namespace, system_name)
        self.ListenForEvent('CustomSwordMod', 'AnimationClient', 'AttackedPacket', self, self.attacked)
        namespace = serverApi.GetEngineNamespace()
        system_name = serverApi.GetEngineSystemName()
        self.ListenForEvent(namespace, system_name, 'StartDestroyBlockServerEvent', self, self.attack_click_block)
        self.player_attacked_cache = {}
        self.attack_type = ['start', 'will_hit', 'end']

    def attacked(self, event):
        _type = event['type']
        player_id = event['playerId']
        self.player_attacked_cache[player_id] = _type
        if _type == 'will_hit':
            entities = compFactory.CreateGame(player_id).GetEntitiesAround(player_id, 6, {
                    'any_of': {
                            'test': 'is_family',
                            'subject': 'other',
                            'operator': 'not',
                            'value': 'instabuild'
                            }
                    })
            for entity in entities:
                self.sector_attack(player_id, entity, 65.0, 6.0, 7, attacker_id=player_id)
        elif _type == 'start':
            players = compFactory.CreatePlayer(player_id).GetRelevantPlayer([player_id])
            self.NotifyToMultiClients(players, 'AttackSync', {
                    'playerId': player_id,
                    'value': 1.0
                    })
        else:
            players = compFactory.CreatePlayer(player_id).GetRelevantPlayer([player_id])
            self.NotifyToMultiClients(players, 'AttackSync', {
                    'playerId': player_id,
                    'value': 0.0
                    })

    def attack_click_block(self, event):
        player_id = event['playerId']
        if self.player_attacked_cache.get(player_id, '') != 'end':
            event['cancel'] = True

    def sector_attack(self, attacker, victim, between_angle=0.0, radius=0.0, damage=0, cause=serverApi.GetMinecraftEnum().ActorDamageCause.EntityAttack, attacker_id=None, child_attacker_id=None, knock=True):
        attacker_foot_pos = compFactory.CreatePos(attacker).GetFootPos()
        victim_foot_pos = compFactory.CreatePos(victim).GetFootPos()
        delta = Vector3(victim_foot_pos) - Vector3(attacker_foot_pos)
        forward_vector = serverApi.GetDirFromRot(compFactory.CreateRot(attacker).GetRot())
        angle = math.degrees(math.acos(Vector3.Dot(delta.Normalized(), Vector3(forward_vector).Normalized())))
        if angle < between_angle and delta.Length() < radius:
            compFactory.CreateHurt(victim).Hurt(damage, cause, attacker_id, child_attacker_id, knock)
