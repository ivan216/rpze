# -*- coding: utf_8 -*-   
import basic.inject as inject
from tests import basic_test
from time import sleep
from rp_extend import Controller

if __name__ == "__main__":
    pids = inject.open_game(r"G:\pvz\en\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe")
    inject.inject(pids)
    ctler = Controller(pids[0])
    basic_test(ctler)