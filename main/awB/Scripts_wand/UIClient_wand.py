# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from Scripts_wand.sys_wand import MOD_UI_CLS_PATH
import math
compFactory = clientApi.GetEngineCompFactory()

ScreenNode = clientApi.GetScreenNodeCls()


class Main(ScreenNode):

    def __init__(self, namespace, name, params):
        ScreenNode.__init__(self, namespace, name, params)

        # 由于使用CreateUi来创建界面，与PushScreen界面不同的是，主路径在最前面需要加一个/
        self.progress_path = "/health_image"
        self.clientSystem = clientApi.GetSystem("wand", "wandClient")

    def Create(self):
        #按钮区
        self.AddTouchEventHandler("/panel/shoot", self.shoot,{"isSwallow": True})
        self.AddTouchEventHandler("/panel/shoot2", self.shoot2,{"isSwallow": True})
    
    def shoot(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchDown or touchEvent == touchEventEnum.TouchMove:
            self.clientSystem.shoot_on(True)
        if touchEvent == touchEventEnum.TouchUp or touchEvent == touchEventEnum.TouchCancel:
            self.clientSystem.shoot_on(False)
            
    def shoot2(self, args):
        touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
        touchEvent = args["TouchEvent"]
        if touchEvent == touchEventEnum.TouchUp:
            self.clientSystem.magic()
            
