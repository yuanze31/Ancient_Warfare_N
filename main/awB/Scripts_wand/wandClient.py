# -*- coding: UTF-8 -*-
from mod.client.system.clientSystem import ClientSystem
import mod.client.extraClientApi as clientApi
from Scripts_wand.sys_wand import MOD_UI_CLS_PATH
import math
import random
import time
compFactory = clientApi.GetEngineCompFactory()

class Main(ClientSystem):

    def __init__(self, namespace, system_name):
        ClientSystem.__init__(self, namespace, system_name)
        namespace, system = clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName()
        #全局
        self.mPlayerId = clientApi.GetLocalPlayerId()#玩家id
        self.wands = ["aw:ice_wand","aw:fire_wand"]
        self.wand_screen=None
        self.shoot_p=False
        self.bulidup=0
        
        #监听自身
        self.ListenForEvent(namespace, system,
                            'OnLocalPlayerStopLoading', self, self.client_init)#注册玩家动画结点用
        self.ListenForEvent(namespace, system, 'UiInitFinished', self, self.ui_loaded)
        self.ListenForEvent(namespace, system, 'OnCarriedNewItemChangedClientEvent', self, self.change_wand)#切换物品时
        self.ListenForEvent(namespace, system, 'LeftClickBeforeClientEvent', self, self.LeftClickB)#点击左键
        #self.ListenForEvent(namespace, system, 'LeftClickReleaseClientEvent', self, self.LeftClickR)#松开左键
        self.ListenForEvent(namespace, system, 'RightClickBeforeClientEvent', self, self.RightClickB)#点击右键
        self.ListenForEvent(namespace, system, 'RightClickReleaseClientEvent', self, self.RightClickR)#松开右键
        #监听sever端
        self.ListenForEvent('wand', 'wandServer','bullet_hit', self, self.bullet_hit)#magic击中

    #方便电脑测试
    def RightClickB(self,data):
        # print("ok")
        Icomp = compFactory.CreateItem(self.mPlayerId)
        carriedData = Icomp.GetCarriedItem()
        if carriedData:
            if carriedData["newItemName"]=="aw:ice_wand" or carriedData["newItemName"]=="aw:fire_wand":
                data["cancel"]=True
                self.shoot_on(True)
                # print("right")
    def RightClickR(self,data):
        self.shoot_on(False)
        # print("right1")
        
    def LeftClickB(self,data):
        Icomp = compFactory.CreateItem(self.mPlayerId)
        carriedData = Icomp.GetCarriedItem()
        if carriedData:
            if carriedData["newItemName"]=="aw:ice_wand" or carriedData["newItemName"]=="aw:fire_wand":
                data["cancel"]=True
                self.magic()

    #注册节点和导入动画
    def client_init(self,data):
        playerId = clientApi.GetLocalPlayerId()
        #攻击和技能节点
        query_comp = compFactory.CreateQueryVariable(clientApi.GetLevelId())
        query_comp.Register("query.mod.ice_hold", 0.0)
        query_comp.Register("query.mod.fire_hold", 0.0)
        query_comp.Register("query.mod.fire", 0.0)
        query_comp.Register("query.mod.destroy", 0.0)
        #动画      
        actor_comp = compFactory.CreateActorRender(clientApi.GetLocalPlayerId())
        actor_comp.AddPlayerAnimationController(
                'controller.wand.run',
                'controller.animation.wand.run'
            )
        actor_comp.AddPlayerAnimationIntoState('root', 'first_person', 'controller.wand.run',
            "query.mod.ice_hold||query.mod.fire_hold")
        actor_comp.AddPlayerAnimation("hold","animation.wand.hold")
        actor_comp.AddPlayerAnimation("fire","animation.wand.fire")
        actor_comp.AddPlayerAnimation("destroy","animation.wand.destroy")
        actor_comp.AddPlayerAnimationIntoState('controller.wand.run', 'default', "hold")
        actor_comp.AddPlayerAnimationIntoState('controller.wand.run', 'fire', "fire")
        actor_comp.AddPlayerAnimationIntoState('controller.wand.run', 'destroy', "destroy")
        #模型和贴图资源
        kk2 = actor_comp.AddPlayerGeometry("ice_wand_model", "geometry.ice_wand")
        actor_comp.AddPlayerTexture("ice_wand_model", "textures/entity/ice_wand")
        actor_comp.AddPlayerGeometry("fire_wand_model", "geometry.fire_wand")
        actor_comp.AddPlayerTexture("fire_wand_model", "textures/entity/fire_wand")
        actor_comp.RebuildPlayerRender()
        #渲染器
        kk = actor_comp.AddPlayerRenderController("controller.render.ice_wand","query.mod.ice_hold")
        actor_comp.AddPlayerRenderController("controller.render.fire_wand","query.mod.fire_hold")
        actor_comp.RebuildPlayerRender()
        print("冰之张：{}：{}".format(kk,kk2))
            

    #使用动画节点
    def query_play(self,data):
        eid = data["eid"]
        query_name = data["query_name"]
        play = data["play"]
        query_comp = compFactory.CreateQueryVariable(clientApi.GetLevelId())
        query_comp = compFactory.CreateQueryVariable(eid)
        query_comp.Set(query_name, play)

    # 客户端ui加载完毕
    def ui_loaded(self, event):
        print "client模板建立"
        clientApi.RegisterUI('wand', 'wand_screen', MOD_UI_CLS_PATH, 'zt.wand_screen') 
        
    #shoot_on,shoot,shoot_2是持续武器    
    def shoot_on(self,data):
        if data:
            self.shoot_p=data
            self.shoot()
        else:
            self.shoot_p=data
            self.query_play({"eid":self.mPlayerId ,"query_name":"query.mod.destroy","play":0.0})
            
    def shoot(self):
        if not self.shoot_p:
            print(self.shoot_p)
            return
        playerId=self.mPlayerId    
        Icomp = compFactory.CreateItem(playerId)
        carriedData = Icomp.GetCarriedItem()
        pos = self.GetEntityRot(playerId,1)
        gameComp = compFactory.CreateGame(clientApi.GetLevelId())
        if not carriedData:
            return
        if carriedData["newItemName"]=="aw:ice_wand":
            #播放特效音效，发送服务端事件,动作动画
            gameComp.AddTimer(0.5, self.NotifyToServer,"ice_spring",{"playerId":self.mPlayerId})#冰泉
            self.unleash_sfx({"sfx":"effects/bingdong.json","pos":pos,"time":2})
            self.play_music({"music_name":"bingdong","eid":playerId,"pos":(0,0,0)})
            self.query_play({"eid":playerId,"query_name":"query.mod.destroy","play":1.0})
            print("冰泉")
        else:
            gameComp.AddTimer(0.5,self.NotifyToServer,"slow_burn",{"playerId":self.mPlayerId})#野火燎原
            x,y,z = pos
            self.unleash_sfx({"sfx":"effects/FireBlooms.json","pos":(x,y-0.5,z),"time":2})
            self.play_music({"music_name":"firepense","eid":playerId,"pos":(0,0,0)})
            self.query_play({"eid":playerId,"query_name":"query.mod.destroy","play":1.0})
        gameComp.AddTimer(0.3, self.shoot_2)  

    def shoot_2(self):
        if self.shoot_p:
            self.shoot()
            print("shoot_p")
 
    def magic(self):
        print("magic")
        Icomp = compFactory.CreateItem(self.mPlayerId)
        carriedData = Icomp.GetCarriedItem()
        if not carriedData:
            return
        gameComp = compFactory.CreateGame(clientApi.GetLevelId())    
        if carriedData["newItemName"]=="aw:ice_wand":
            pass
            #播放音效，发送服务端事件
            self.NotifyToServer("bullet",{"playerId":self.mPlayerId,"type":"ice"})#ice
            self.play_music({"music_name":"bingfase","eid":self.mPlayerId,"pos":(0,0,0)})
            self.query_play({"eid":self.mPlayerId,"query_name":"query.mod.fire","play":1.0})
            gameComp.AddTimer(0.43,self.query_play,{"eid":self.mPlayerId,"query_name":"query.mod.fire","play":0.0})
        else:
            self.NotifyToServer("bullet",{"playerId":self.mPlayerId,"type":"fire"})#fire  
            self.play_music({"music_name":"firefase","eid":self.mPlayerId,"pos":(0,0,0)})
            self.query_play({"eid":self.mPlayerId,"query_name":"query.mod.fire","play":1.0})
            gameComp.AddTimer(0.43,self.query_play,{"eid":self.mPlayerId,"query_name":"query.mod.fire","play":0.0})
            

    def bullet_hit(self,data):
        if data["type"]=="ice":
            self.unleash_sfx({"sfx":"effects/ice_z.json","pos":data["pos"],"time":0.5})
            self.play_music({"music_name":"bingsui","eid":data["targetId"],"pos":(0,0,0)})
        else:
            self.unleash_sfx({"sfx":"effects/fire_z.json","pos":data["pos"],"time":0.5})
        
    def change_wand(self,data):
        itemDict = data["itemDict"]
        playerId =  clientApi.GetLocalPlayerId()
        if not itemDict:
            self.query_play({"eid":playerId,"query_name":"query.mod.ice_hold","play":0.0})
            self.query_play({"eid":playerId,"query_name":"query.mod.fire_hold","play":0.0})
            if self.wand_screen:
                self.wand_screen.SetRemove()
                self.wand_screen = None
            return
        item_name = itemDict["newItemName"]
        #武器节点
        if item_name=="aw:ice_wand":
            self.query_play({"eid":playerId,"query_name":"query.mod.ice_hold","play":1.0})
            self.query_play({"eid":playerId,"query_name":"query.mod.fire_hold","play":0.0})
        elif item_name=="aw:fire_wand":
            self.query_play({"eid":playerId,"query_name":"query.mod.fire_hold","play":1.0})
            self.query_play({"eid":playerId,"query_name":"query.mod.ice_hold","play":0.0})
        if item_name in self.wands:
            if self.wand_screen:
                return
            else:
                self.wand_screen = clientApi.CreateUI('wand','wand_screen',{"isHud": 1})
        else:
            self.query_play({"eid":playerId,"query_name":"query.mod.ice_hold","play":0.0})
            self.query_play({"eid":playerId,"query_name":"query.mod.fire_hold","play":0.0})
            if self.wand_screen:
                self.wand_screen.SetRemove()
                self.wand_screen = None
 
    #特效
    def unleash_sfx(self,data):
        playerId = self.mPlayerId
        sfx = data["sfx"]
        pos = data["pos"]
        time = data["time"]
        particleEntityId = self.CreateEngineParticle(sfx, pos)
        particleControlComp = compFactory.CreateParticleControl(particleEntityId)
        
        # 绕y轴旋转kk度
        compRot = compFactory.CreateRot(playerId)
        ud,lr = compRot.GetRot()
        x,y,z = clientApi.GetDirFromRot((ud,lr))
        #asd
        PTcomp = compFactory.CreateParticleTrans(particleEntityId)
        if x>=0.92:
            kk = 180
        elif x>0 and z>0:
            kk = x*100+z*100
        elif  x>0 and z<0:
            kk = -(x*100+abs(z)*100)
        else:
            kk = z*100
        PTcomp.SetRotUseZXY((0, kk, 0))
        particleControlComp.Play()
        #销毁网易特效
        gameComp = compFactory.CreateGame(clientApi.GetLevelId())
        gameComp.AddTimer(time, particleControlComp.Stop)

    def GetEntityRot(self,entityId,pLen):
        #计算生物视角前位置
        compPos = compFactory.CreatePos(entityId)
        x,y,z = compPos.GetPos()
        compRot = compFactory.CreateRot(entityId)
        ud,lr = compRot.GetRot()
        a=(lr%360)*math.pi/180.0
        b=ud*math.pi/180.0
        xi=-math.sin(a)*math.cos(b)*pLen
        yi=-math.sin(b)
        zi=math.cos(a)*math.cos(b)*pLen
        return (x+xi,y+yi,z+zi)       

    #play_music    
    def play_music(self,data):
        music_name = data["music_name"]
        eid = data["eid"]
        pos = data["pos"]
        CreateCcomp = compFactory.CreateCustomAudio(clientApi.GetLevelId())
        musicId = CreateCcomp.PlayCustomMusic(music_name, pos, 1, 1, False, eid)
 
    #暂时不用            
    def bulidup_w(self):
        bUc= self.wand_screen.GetBaseUIControl("/panel/boostbar_panel")
        param = {'power':3*self.bulidup,'gravity':0.05}
        self.NotifyToServer("shoot",{"playerId":self.mPlayerId,"param":param})
        self.bulidup=0
        bUc.SetVisible(self.shoot_p)
        imageC= self.wand_screen.GetBaseUIControl("/panel/boostbar_panel/pf").asImage()
        imageC.SetSpriteClipRatio(1.0)                  