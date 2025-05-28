# -*- coding: utf-8 -*-

from common.mod import Mod


@Mod.Binding(name="Script_NeteaseModGuAmt7p8", version="0.0.1")
class Script_NeteaseModGuAmt7p8(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def Script_NeteaseModGuAmt7p8ServerInit(self):
        pass

    @Mod.DestroyServer()
    def Script_NeteaseModGuAmt7p8ServerDestroy(self):
        pass

    @Mod.InitClient()
    def Script_NeteaseModGuAmt7p8ClientInit(self):
        pass

    @Mod.DestroyClient()
    def Script_NeteaseModGuAmt7p8ClientDestroy(self):
        pass
