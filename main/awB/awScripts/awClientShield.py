# -*- coding: utf-8 -*-
from QuModLibs.Client import *

CF = clientApi.GetEngineCompFactory()


@AllowCall
def showShieldSuccessEffect(dimensionId, pos):
    if dimensionId == CF.CreateGame(levelId).GetCurrentDimension():
        print CF.CreateCustomAudio(levelId).PlayCustomMusic("item.shield.block", pos, 0.2, 1, False)
