# -*- coding: utf-8 -*-

from Preset.Model.PartBase import PartBase
from Preset.Model.GameObject import registerGenericClass

@registerGenericClass('changeskinPart')
class changeskinPart(PartBase):

    def __init__(self):
        super(changeskinPart, self).__init__()
        self.name = '蓝图零件'
        self.description = '蓝图零件'
        self.bpFiles = ['changeskinPart.bp']
        self.replicated = []
