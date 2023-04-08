# -*- coding: utf-8 -*-

from Preset.Model.PartBase import PartBase
from Preset.Model.GameObject import registerGenericClass

@registerGenericClass('basicenvironmentPart')
class basicenvironmentPart(PartBase):

    def __init__(self):
        super(basicenvironmentPart, self).__init__()
        self.name = '蓝图零件'
        self.description = '蓝图零件'
        self.bpFiles = ['basicenvironmentPart.bp']
        self.replicated = []

    def InitServer(self):
        return PartBase.InitServer(self)
