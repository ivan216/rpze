# -*- coding: utf_8 -*-
"""
子弹相关的枚举和类
"""
from enum import IntEnum
from typing import Self

from .obj_base import ObjNode, property_i32, property_f32, property_bool, property_int_enum, ObjId, obj_list
from ..basic import asm


class ProjectileType(IntEnum):
    """
    子弹类型
    """
    pea = 0x0
    snow_pea = 0x1
    cabbage = 0x2
    melon = 0x3
    puff = 0x4
    wintermelon = 0x5
    fire_pea = 0x6
    star = 0x7
    cactus = 0x8
    basketball = 0x9
    kernel = 0xA
    cob_cannon = 0xB
    butter = 0xC


class ProjectileMotionType(IntEnum):
    """
    子弹运动类型
    """
    straight = 0
    parabola = 1
    switch_way = 2
    puff = 5
    left_straight = 6
    starfruit = 7
    cattail = 9


class Projectile(ObjNode):
    """
    子弹对象
    """
    ITERATOR_FUNC_ADDRESS = 0x41C9B0

    OBJ_SIZE = 0x94

    int_x = property_i32(0x8, "图像整数 x 坐标")

    int_y = property_i32(0xc, "图像整数 y 坐标")

    col = property_i32(0x1c, "所在行数")

    x = property_f32(0x30, "浮点 x 坐标")

    y = property_f32(0x34, "浮点 y 坐标")

    dx = property_f32(0x3c, "x 速度")

    dy = property_f32(0x40, "y 速度")

    is_dead = property_bool(0x50, "是否死亡")

    type_ = property_int_enum(0x5c, ProjectileType, "子弹类型")

    motion_type = property_int_enum(0x58, ProjectileMotionType, "子弹运动类型")

    @property
    def target_zombie_id(self) -> ObjId:
        """香蒲子弹目标僵尸"""
        return ObjId(self.base_ptr + 0x88, self.controller)

    def die(self) -> None:
        """
        令自己死亡
        """
        code = f"""
            mov eax, {self.base_ptr}
            call {0x46EB20}  // Projectile::Die
            ret"""
        asm.run(code, self.controller)


class ProjectileList(obj_list(Projectile)):
    """
    子弹 DataArray
    """
    def free_all(self) -> Self:
        code = f"""
                push edi   
                push esi
                mov eax, [0x6a9ec0]
                mov edi, [eax + 0x768]
                mov esi, {self.controller.result_address}
                xor edx, edx
                mov [esi], edx
                LIterate:
                    mov {Projectile.ITERATOR_P_BOARD_REG}, edi
                    call {Projectile.ITERATOR_FUNC_ADDRESS}  // Board::IterateProjectile
                    test al, al
                    jz LFreeAll
                    mov eax, [esi]
                    call {0x46EB20}  // Projectile::Die
                    jmp LIterate
                    
                LFreeAll:
                    mov edi, {self.base_ptr}
                    call {0x41e600}  // DataArray<Zombie>::DataArrayFreeAll
                    pop esi
                    pop edi
                    ret"""
        asm.run(code, self.controller)
        return self
