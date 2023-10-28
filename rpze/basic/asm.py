# -*- coding: utf_8 -*- 
from rp_extend import Controller
import keystone as ks


def run(code: str, controller: Controller) -> bool:
    """
    执行code汇编码
    
    Args:
        code: x86 intel格式汇编字符串, 应该以一个(void) -> void函数, 即以"ret"结尾并且做栈平衡
        controller: Controller对象, 用于执行汇编码
    Returns:
        执行成功返回True
    """
    r = decode(code)
    controller.run_code(r, len(r))
    

def decode(code: str) -> bytes:
    """
    解码code汇编码
    Args:
        code: code: x86 intel格式汇编字符串
    Returns:
        解码后的字节码
    Raises:
        RuntimeError: 汇编码错误
    """
    try:
        k = ks.Ks(ks.KS_ARCH_X86, ks.KS_MODE_32)
        asm, _ = k.asm(code, as_bytes=True)
        return asm
    except ks.KsError as e:
        raise RuntimeError(f"asm error, {e}") from e
