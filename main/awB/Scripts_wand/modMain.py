# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi


@Mod.Binding(name="wand", version="0.1")
class modMain(object):

    def __init__(self):
        pass

    @Mod.InitClient()
    def initClient(self):
        clientApi.RegisterSystem("wand", "wandClient", "Scripts_wand.wandClient.Main")

    @Mod.InitServer()
    def initServer(self):
        serverApi.RegisterSystem("wand", "wandServer", "Scripts_wand.wandServer.Main")

    @Mod.DestroyClient()
    def destroyClient(self):
        pass

    @Mod.DestroyServer()
    def destroyServer(self):
        pass
