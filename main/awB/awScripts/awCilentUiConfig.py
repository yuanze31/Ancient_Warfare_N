# -*- coding: utf-8 -*-

from QuModLibs.Client import *
from QuModLibs.UI import ScreenNodeWrapper

CF = clientApi.GetEngineCompFactory()

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()

ConfigCache = {}


def requestAllConfig():
    Call("cilentRequestConfig", playerId)


@AllowCall
def syncCilentConfigCache(configDict):
    global ConfigCache
    # print "客户端更新配置缓存：" + str(configDict)
    ConfigCache = configDict


@ScreenNodeWrapper.autoRegister("configUI.main")
class configUI(ScreenNodeWrapper):
    def __init__(self, namespace, name, param):
        ScreenNodeWrapper.__init__(self, namespace, name, param)
        # print("界面对象构造完毕，此时还未完成绘制，不得操作控件")
        pass

    def Create(self):
        ScreenNodeWrapper.Create(self)
        # print("UI绘制完毕，此时可以操作控件对象")
        scrollViewPath = self.GetBaseUIControl("/mainPanel/bg/mainScrollView").asScrollView().GetScrollViewContentPath()
        spawnAllPath = "/linearLayout/spawnAll/linearLayout/switch"
        spawnBanditPath = "/linearLayout/spawnBandit/linearLayout/switch"
        spawnDesertPath = "/linearLayout/spawnDesert/linearLayout/switch"
        spawnNativePath = "/linearLayout/spawnNative/linearLayout/switch"
        spawnPiratePath = "/linearLayout/spawnPirate/linearLayout/switch"
        spawnPlayerPath = "/linearLayout/spawnPlayer/linearLayout/switch"
        spawnVikingPath = "/linearLayout/spawnViking/linearLayout/switch"

        spawnAllSwitch = self.GetBaseUIControl(scrollViewPath + spawnAllPath).asSwitchToggle()
        spawnBanditSwitch = self.GetBaseUIControl(scrollViewPath + spawnBanditPath).asSwitchToggle()
        spawnDesertSwitch = self.GetBaseUIControl(scrollViewPath + spawnDesertPath).asSwitchToggle()
        spawnNativeSwitch = self.GetBaseUIControl(scrollViewPath + spawnNativePath).asSwitchToggle()
        spawnPirateSwitch = self.GetBaseUIControl(scrollViewPath + spawnPiratePath).asSwitchToggle()
        spawnPlayerSwitch = self.GetBaseUIControl(scrollViewPath + spawnPlayerPath).asSwitchToggle()
        spawnVikingSwitch = self.GetBaseUIControl(scrollViewPath + spawnVikingPath).asSwitchToggle()

        allow_spawn = ConfigCache["allow_spawn"]
        camp_spawn = ConfigCache["camp_spawn"]
        soldier_name = ConfigCache["soldier_name"]

        spawnAllSwitch.SetToggleState(allow_spawn)
        spawnBanditSwitch.SetToggleState(bool(camp_spawn[0]))
        spawnDesertSwitch.SetToggleState(bool(camp_spawn[1]))
        spawnNativeSwitch.SetToggleState(bool(camp_spawn[2]))
        spawnPirateSwitch.SetToggleState(bool(camp_spawn[3]))
        spawnPlayerSwitch.SetToggleState(bool(camp_spawn[4]))
        spawnVikingSwitch.SetToggleState(bool(camp_spawn[5]))

        @self.bindButtonClickHandler("/mainPanel/bg/saveAndCancel/cancel")
        def onCancelButtonClick():
            self.removeClsUI()
            hideGameUI(False)

        @self.bindButtonClickHandler("/mainPanel/bg/saveAndCancel/save")
        def onSaveButtonClick():
            new_allow_spawn = spawnAllSwitch.GetToggleState()
            new_camp_spawn = [spawnBanditSwitch.GetToggleState(), spawnDesertSwitch.GetToggleState(), spawnNativeSwitch.GetToggleState(), spawnPirateSwitch.GetToggleState(), spawnPlayerSwitch.GetToggleState(), spawnVikingSwitch.GetToggleState()]
            new_soldier_name = soldier_name
            newConfigDict = {
                    "allow_spawn": new_allow_spawn,
                    "camp_spawn": new_camp_spawn,
                    "soldier_name": new_soldier_name
                    }
            Call("cilentConfigUISave", playerId, newConfigDict)
            self.removeClsUI()
            hideGameUI(False)


@AllowCall
def createConfigUI():
    configUI.createUI("", {
            "isHud": 0
            })
    hideGameUI(True)


def hideGameUI(disable=True):
    clientApi.HideAirSupplyGUI(disable)
    clientApi.HideArmorGui(disable)
    clientApi.HideChangePersonGui(disable)
    clientApi.HideChatGUI(disable)
    clientApi.HideEmoteGUI(disable)
    clientApi.HideExpGui(disable)
    clientApi.HideFoldGUI(disable)
    clientApi.HideHealthGui(disable)
    clientApi.HideHorseHealthGui(disable)
    # clientApi.HideHudGUI(disabled)
    clientApi.HideHungerGui(disable)
    clientApi.HideInteractGui(disable)
    clientApi.HideJumpGui(disable)
    clientApi.HideMoveGui(disable)
    clientApi.HideNeteaseStoreGui(disable)
    clientApi.HidePauseGUI(disable)
    clientApi.HideSlotBarGui(disable)
    clientApi.HideSneakGui(disable)
    clientApi.HideVoiceGUI(disable)
    clientApi.HideWalkGui(disable)
    interact = not disable
    # clientApi.SetResponse(interact)
    CF.CreateOperation(levelId).SetCanMove(interact)  # if disable:  #     CF.CreateCamera(levelId).LockCamera((CF.CreateCamera(levelId).GetPosition()), CF.CreateCamera(levelId).GetCameraRotation()[:2])  # else:  #     CF.CreateCamera(levelId).UnLockCamera()


requestAllConfig()
