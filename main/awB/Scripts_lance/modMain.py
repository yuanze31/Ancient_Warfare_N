# -*- coding: UTF-8 -*-

import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
from mod.common.mod import Mod


@Mod.Binding(name="CustomSwordMod", version="0.1")
class CustomSwordMod(object):

    def __init__(self):
        pass

    @Mod.InitClient()
    def init_client(self):
        clientApi.RegisterSystem("CustomSwordMod", "AnimationClient", "Scripts_lance.client.AnimationClient")

    @Mod.InitServer()
    def init_server(self):
        serverApi.RegisterSystem("CustomSwordMod", "AnimationServer", "Scripts_lance.server.AnimationServer")

    @Mod.DestroyClient()
    def destroy_client(self):
        pass

    @Mod.DestroyServer()
    def destroy_server(self):
        pass
