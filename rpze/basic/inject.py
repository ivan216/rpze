﻿import win32gui as wing
import win32process as winp
import os
import subprocess


def find_window(window_name) -> int:
    """
    返回名称为str的窗口主进程pid
    """
    handle = wing.FindWindow(None, window_name)
    _, pid = winp.GetWindowThreadProcessId(handle)
    return pid


def open_game(game_path: str, num=1) -> list[int]:
    """
    通过路径, 将pvz作为python子进程打开游戏, 返回num个的列表pids
    """
    abs_path = os.path.abspath(game_path)
    route, exe_name = os.path.split(abs_path)
    current_directory = os.getcwd()
    os.chdir(route)
    ret = [0] * num
    for i in range(num):
        process = subprocess.Popen(f"\"{exe_name}\"")
        ret[i] = process.pid
    os.chdir(current_directory)
    return ret


def inject(pids: list[int]):
    """
    注入dll, pids为pid列表
    """
    dll_path = os.path.abspath(".\\bin\\rp_dll.dll")
    s = f'.\\bin\\rp_injector.exe \"{dll_path}\" {len(pids)} '
    for i in pids:
        s += str(i)
        s += ' '

    os.system(s)
