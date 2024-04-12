# -*- coding: UTF-8 -*-
from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi


@Mod.Binding(name="CustomSwordMod", version="0.1")
class CustomSwordMod(object):

    def __init__(self):
        pass

    @Mod.InitClient()
    def init_client(self):
        clientApi.RegisterSystem("CustomSwordMod", "AnimationClient",
                                 "CustomSwordScripts.client.AnimationClient")

    @Mod.InitServer()
    def init_server(self):
        serverApi.RegisterSystem("CustomSwordMod", "AnimationServer",
                                 "CustomSwordScripts.server.AnimationServer")

    @Mod.DestroyClient()
    def destroy_client(self):
        pass

    @Mod.DestroyServer()
    def destroy_server(self):
        pass
