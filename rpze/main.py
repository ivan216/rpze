# -*- coding: utf_8 -*-

from src.rpze.basic.inject import InjectedGame
from src.rpze.basic.inject import enter_ize
from src.rpze.examples.botanical_clock import botanical_clock
from src.rpze.structs import get_board

with InjectedGame(r"C:\space\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    ctler = game.controller
    # get_board(ctler)
    enter_ize(game)
    botanical_clock(ctler, True)
