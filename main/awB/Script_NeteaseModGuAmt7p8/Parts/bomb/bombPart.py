# -*- coding: utf-8 -*-

from Preset.Model.PartBase import PartBase
from Preset.Model.GameObject import registerGenericClass

@registerGenericClass('bombPart')
class bombPart(PartBase):

    def __init__(self):
        super(bombPart, self).__init__()
        self.name = '蓝图零件'
        self.description = '蓝图零件'
        self.bpFiles = ['bombPart.bp']
        self.replicated = []

    def DestroyServer(self):
        return PartBase.DestroyServer(self)

    def InitClient(self):
        return PartBase.InitClient(self)

    def TickServer(self):
        return PartBase.TickServer(self)

    def InitServer(self):
        return PartBase.InitServer(self)

    def TickClient(self):
        return PartBase.TickClient(self)

    def DestroyClient(self):
        return PartBase.DestroyClient(self)
