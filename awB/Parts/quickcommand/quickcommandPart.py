# -*- coding: utf-8 -*-

from Preset.Model.PartBase import PartBase
from Preset.Model.GameObject import registerGenericClass

@registerGenericClass('quickcommandPart')
class quickcommandPart(PartBase):

    def __init__(self):
        super(quickcommandPart, self).__init__()
        self.name = '蓝图零件'
        self.description = '蓝图零件'
        self.bpFiles = ['quickcommandPart.bp']
        self.replicated = []

    def InitServer(self):
        return PartBase.InitServer(self)

    def InitClient(self):
        return PartBase.InitClient(self)
