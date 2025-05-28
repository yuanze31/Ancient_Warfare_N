# -*- coding: UTF-8 -*-
import time

import mod.client.extraClientApi as clientApi

compFactory = clientApi.GetEngineCompFactory()
ClientSystem = clientApi.GetClientSystemCls()


class AnimationClient(ClientSystem):

    def __init__(self, namespace, system_name):
        ClientSystem.__init__(self, namespace, system_name)
        namespace = clientApi.GetEngineNamespace()
        system_name = clientApi.GetEngineSystemName()
        self.ListenForEvent(namespace, system_name, 'OnLocalPlayerStopLoading', self, self.client_init)
        self.ListenForEvent(namespace, system_name, 'LeftClickBeforeClientEvent', self, self.attack_click)
        self.ListenForEvent(namespace, system_name, 'TapBeforeClientEvent', self, self.attack_click)
        self.ListenForEvent(namespace, system_name, 'StartDestroyBlockClientEvent', self, self.attack_click_block)
        self.ListenForEvent('CustomSwordMod', 'AnimationServer', 'AttackedSync', self, self.attacked_sync)
        self.click_cooldown = time.time()

    def client_init(self, event):
        player_id = clientApi.GetLocalPlayerId()
        query_comp = compFactory.CreateQueryVariable(clientApi.GetLevelId())
        query_comp.Register('query.mod.sword_attack_time', 0.0)
        query_comp = compFactory.CreateQueryVariable(player_id)
        query_comp.Set('query.mod.sword_attack_time', 0.0)
        actor_comp = compFactory.CreateActorRender(clientApi.GetLocalPlayerId())
        actor_comp.AddPlayerAnimation('sword_third_hold', 'animation.lance.third_hold')
        actor_comp.AddPlayerAnimation('third_arm_attack', 'animation.lance.third_arm_attack')
        actor_comp.AddPlayerAnimationController('controller.third_person_attack_fixed', 'controller.animation.player.third_person_attack_fixed')
        actor_comp.AddPlayerAnimationIntoState('root', 'third_person', 'sword_third_hold', "query.get_equipped_item_full_name('main_hand') == 'aw:wooden_lance'")
        actor_comp.AddPlayerAnimationIntoState('root', 'third_person', 'controller.third_person_attack_fixed', "query.get_equipped_item_full_name('main_hand') == 'aw:wooden_lance'")
        actor_comp.AddPlayerAnimationIntoState('root', 'third_person', 'sword_third_hold', "query.get_equipped_item_full_name('main_hand') == 'aw:stone_lance'")
        actor_comp.AddPlayerAnimationIntoState('root', 'third_person', 'controller.third_person_attack_fixed', "query.get_equipped_item_full_name('main_hand') == 'aw:stone_lance'")
        actor_comp.AddPlayerAnimationIntoState('root', 'third_person', 'sword_third_hold', "query.get_equipped_item_full_name('main_hand') == 'aw:iron_lance'")
        actor_comp.AddPlayerAnimationIntoState('root', 'third_person', 'controller.third_person_attack_fixed', "query.get_equipped_item_full_name('main_hand') == 'aw:iron_lance'")
        actor_comp.AddPlayerAnimationIntoState('root', 'third_person', 'sword_third_hold', "query.get_equipped_item_full_name('main_hand') == 'aw:golden_lance'")
        actor_comp.AddPlayerAnimationIntoState('root', 'third_person', 'controller.third_person_attack_fixed', "query.get_equipped_item_full_name('main_hand') == 'aw:golden_lance'")
        actor_comp.AddPlayerAnimationIntoState('root', 'third_person', 'sword_third_hold', "query.get_equipped_item_full_name('main_hand') == 'aw:diamond_lance'")
        actor_comp.AddPlayerAnimationIntoState('root', 'third_person', 'controller.third_person_attack_fixed', "query.get_equipped_item_full_name('main_hand') == 'aw:diamond_lance'")
        actor_comp.AddPlayerAnimationIntoState('root', 'third_person', 'sword_third_hold', "query.get_equipped_item_full_name('main_hand') == 'aw:netherite_lance'")
        actor_comp.AddPlayerAnimationIntoState('root', 'third_person', 'controller.third_person_attack_fixed', "query.get_equipped_item_full_name('main_hand') == 'aw:netherite_lance'")
        actor_comp.RebuildPlayerRender()

    def attack_click(self, event):
        current_time = time.time()
        carried_item = compFactory.CreateItem(clientApi.GetLocalPlayerId()).GetCarriedItem()
        # 在事件响应时计算当前时间扣去过去时间戳是否大于攻击动画的时间，我们的自定义攻击动画时间为0.75秒，因此判断结果需要大于0.75。
        if current_time - self.click_cooldown > 0.75 and carried_item and carried_item['newItemName'] in ["aw:wooden_lance", "aw:stone_lance", "aw:iron_lance", "aw:golden_lance", "aw:diamond_lance", "aw:netherite_lance"]:
            # 继续判断是否满足是金剑，是则重新计算时间戳。
            self.click_cooldown = time.time()
            # 动画开始的时间点
            self.send_attacked_packet(0.0, {
                    'playerId': clientApi.GetLocalPlayerId(),
                    'type': 'start'
                    })
            # 动画打击出伤害的时间点，具体以自定义动画的设计形式为准
            self.send_attacked_packet(0.16, {
                    'playerId': clientApi.GetLocalPlayerId(),
                    'type': 'will_hit'
                    })
            # 动画结束时间点
            self.send_attacked_packet(0.75, {
                    'playerId': clientApi.GetLocalPlayerId(),
                    'type': 'end'
                    })
        else:
            # 正在播放动画时，若重复点击，则取消点击
            if carried_item and carried_item['newItemName'] in ["aw:wooden_lance", "aw:stone_lance", "aw:iron_lance", "aw:golden_lance", "aw:diamond_lance", "aw:netherite_lance"]:
                event['cancel'] = True

    def attack_click_block(self, event):
        player_id = event['playerId']
        if player_id != clientApi.GetLocalPlayerId():
            return
        current_time = time.time()
        if current_time - self.click_cooldown < 0.75:
            event['cancel'] = True

    def attacked_sync(self, event):
        player_id = event['playerId']
        value = event['value']
        compFactory.CreateQueryVariable(player_id).Set('query.mod.sword_attack_time', value)

    def send_attacked_packet(self, _time, data):
        game_comp = compFactory.CreateGame(clientApi.GetLevelId())
        game_comp.AddTimer(_time, self.NotifyToServer, 'AttackedPacket', data)
        game_comp.AddTimer(_time, compFactory.CreateQueryVariable(clientApi.GetLocalPlayerId()).Set, 'query.mod.sword_attack_time', 1.0 if data['type'] == 'start' or data['type'] == 'will_hit' else 0.0)

    def Update(self):
        pass
