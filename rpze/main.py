# -*- coding: utf_8 -*-
import csv

from src.rpze.basic.inject import InjectedGame
from src.rpze.basic.inject import enter_ize
from src.rpze.examples.botanical_clock import botanical_clock

with InjectedGame(r"C:\space\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    ctler = game.controller
    enter_ize(game)
    botanical_clock(ctler, True)

