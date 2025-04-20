# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
from mod.common.mod import Mod


@Mod.Binding(name="aw", version="1.1.0")
class aw(object):

    def __init__(self):
        pass

    @Mod.InitClient()
    def aw_client_init(self):
        clientApi.RegisterSystem("aw", "awClientCilent", "awScripts.awClient.awClientSystem")

    @Mod.InitServer()
    def aw_server_init(self):
        serverApi.RegisterSystem("aw", "awServerSystem", "awScripts.awServer.awServerSystem")

    @Mod.DestroyClient()
    def aw_client_destroy(self):
        pass

    @Mod.DestroyServer()
    def aw_server_destroy(self):
        pass
