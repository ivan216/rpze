# -*- coding: utf_8 -*-
"""
执行编译汇编相关的函数.
"""
from functools import lru_cache

import keystone as ks

from ..rp_extend import Controller


def run(code: str, controller: Controller) -> bool:
    """
    执行code汇编码
    
    Args:
        code: x86 intel格式汇编字符串, 应该是一个(void) -> void函数, 即以"ret"结尾并且保持栈平衡
        controller: Controller对象, 用于执行汇编码
    Returns:
        执行成功返回True
    """
    r = decode(code, controller.asm_address)
    return controller.run_code(r)


__keystone_assembler = ks.Ks(ks.KS_ARCH_X86, ks.KS_MODE_32)


@lru_cache()
def decode(code: str, addr: int = 0) -> bytes:
    """
    解码code汇编码
    
    Args:
        code: x86 intel格式汇编字符串
        addr: 汇编码首字节地址
    Returns:
        解码后的字节码
    """
    asm, _ = __keystone_assembler.asm(code, addr, True)
    return asm
