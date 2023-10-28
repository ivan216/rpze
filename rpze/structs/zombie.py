# -*- coding: utf_8 -*-
"""
僵尸相关的枚举和类
"""
from enum import IntEnum

import structs.obj_base as ob
from basic import asm
from rp_extend import Controller


# 数据结构和pvz_emulator命名保持一致

class ZombieType(IntEnum):
    none = -1,
    zombie = 0x0,
    flag = 0x1,
    conehead = 0x2,
    pole_vaulting = 0x3,
    buckethead = 0x4,
    newspaper = 0x5,
    screendoor = 0x6,
    football = 0x7,
    dancing = 0x8,
    backup_dancer = 0x9,
    ducky_tube = 0xa,
    snorkel = 0xb,
    zomboni = 0xc,
    dolphin_rider = 0xe,
    jack_in_the_box = 0xf,
    balloon = 0x10,
    digger = 0x11,
    pogo = 0x12,
    yeti = 0x13,
    bungee = 0x14,
    ladder = 0x15,
    catapult = 0x16,
    gargantuar = 0x17,
    imp = 0x18,
    giga_gargantuar = 0x20


class ZombieStatus(IntEnum):
    walking = 0x0,
    dying = 0x1,
    dying_from_instant_kill = 0x2,
    dying_from_lawnmower = 0x3,
    bungee_target_drop = 0x4,
    bungee_body_drop = 0x5,
    bungee_idle_after_drop = 0x6,
    bungee_grab = 0x7,
    bungee_raise = 0x8,
    bungee_idle = 0xa,
    pole_vaulting_running = 0xb,
    pole_vaulting_jumping = 0xc,
    pole_vaulting_walking = 0xd,
    rising_from_ground = 0xe,
    jackbox_walking = 0xf,
    jackbox_pop = 0x10,
    pogo_with_stick = 0x14,
    pogo_idle_before_target = 0x15,
    pogo_jump_across = 0x1b,
    newspaper_walking = 0x1d,
    newspaper_destroyed = 0x1e,
    newspaper_running = 0x1f,
    digger_dig = 0x20,
    digger_drill = 0x21,
    digger_lost_dig = 0x22,
    digger_landing = 0x23,
    digger_dizzy = 0x24,
    digger_walk_right = 0x25,
    digger_walk_left = 0x26,
    digger_idle = 0x27,
    dancing_moonwalk = 0x28,
    dancing_point = 0x29,
    dancing_wait_summoning = 0x2a,
    dancing_summoning = 0x2b,
    dancing_walking = 0x2c,
    dancing_armrise1 = 0x2d,
    dancing_armrise2 = 0x2e,
    dancing_armrise3 = 0x2f,
    dancing_armrise4 = 0x30,
    dancing_armrise5 = 0x31,
    backup_spawning = 0x32,
    dolphin_walk_with_dolphin = 0x33,
    dophin_jump_in_pool = 0x34,
    dolphin_ride = 0x35,
    dolphin_jump = 0x36,
    dolphin_walk_in_pool = 0x37,
    dolphin_walk_without_dolphin = 0x38,
    snorkel_walking = 0x39,
    snorkel_jump_in_the_pool = 0x3a,
    snorkel_swim = 0x3b,
    snorkel_up_to_eat = 0x3c,
    snorkel_eat = 0x3d,
    snorkel_finied_eat = 0x3e,
    catapult_shoot = 0x43,
    catapult_idle = 0x44,
    balloon_flying = 0x49,
    balloon_falling = 0x4a,
    balloon_walking = 0x4b,
    imp_flying = 0x47,
    imp_landing = 0x48,
    gargantuar_throw = 0x45,
    gargantuar_smash = 0x46,
    ladder_walking = 0x4c,
    ladder_placing = 0x4d,
    yeti_escape = 0x5b


class ZombieAction(IntEnum):
    none = 0x0,
    entering_pool = 0x1,
    leaving_pool = 0x2,
    caught_by_kelp = 0x3,
    climbing_ladder = 0x6,
    falling = 0x7,
    fall_from_sky = 0x9


class ZombieAccessoriesType1(IntEnum):
    none = 0x0,
    roadcone = 0x1,
    bucket = 0x2,
    football_cap = 0x3,
    miner_hat = 0x4


class ZombieAccessoriesType2(IntEnum):
    none = 0x0,
    screen_door = 0x1,
    newspaper = 0x2,
    ladder = 0x3


class Zombie(ob.ObjNode):
    ITERATOR_FUNC_ADDRESS = 0x41C8F0

    OBJ_SIZE = 0x15c

    int_x: int = ob.property_i32(0x8, "整数x坐标")

    int_y: int = ob.property_i32(0xc, "整数y坐标")

    row: int = ob.property_i32(0x1c, "所在行数")

    type_: ZombieType = ob.property_int_enum(0x24, ZombieType, "僵尸种类")

    status: ZombieStatus = ob.property_int_enum(0x28, ZombieStatus, "僵尸状态")

    x: float = ob.property_f32(0x2c, "浮点x坐标")

    y: float = ob.property_f32(0x30, "浮点y坐标")

    dx: float = ob.property_f32(0x34, "x方向速度")

    is_eating: bool = ob.property_bool(0x51, "在啃食时为True")

    flash_cd: int = ob.property_i32(0x54, """
    发亮倒计时
                                    
    - 刚生成僵尸时为0, 受击变为25
    - 在flash_cd < -500时, 僵尸开始速度重置 + 啃食加速
    """)

    time_since_spawn: int = ob.property_i32(0x60, "出生时间")

    action: ZombieAction = ob.property_int_enum(0x64, ZombieAction, "僵尸行为")

    hp: int = ob.property_i32(0xc8, "本体血量")

    max_hp: int = ob.property_u32(0xcc, "本体血量上限")

    accessories_type_1: ZombieAccessoriesType1 = ob.property_int_enum(
        0xc4, ZombieAccessoriesType1, "一类饰品类型")

    accessories_hp_1: int = ob.property_i32(0xd0, "一类饰品血量")

    accessories_max_hp_1: int = ob.property_i32(0xd4, "一类饰品血量上限")

    accessories_type_2: ZombieAccessoriesType2 = ob.property_int_enum(
        0xd8, ZombieAccessoriesType2, "二类饰品")

    accessories_hp_2: int = ob.property_i32(0xdc, "二类饰品血量")

    accessories_max_hp_2: int = ob.property_i32(0xe0, "二类饰品血量上限")

    hit_box_x: int = ob.property_i32(0x8c, "中弹判定横坐标")

    hit_box_y: int = ob.property_i32(0x90, "中弹判定纵坐标")

    hit_width: int = ob.property_i32(0x94, "中弹判定宽度")

    hit_height: int = ob.property_i32(0x98, "中弹判定高度")

    attack_box_x: int = ob.property_i32(0x9c, "攻击判定横坐标")

    attack_box_y: int = ob.property_i32(0xa0, "攻击判定纵坐标")

    attack_width: int = ob.property_i32(0xa4, "攻击判定宽度")

    attack_height: int = ob.property_i32(0xa8, "攻击判定高度")

    slow_cd: int = ob.property_i32(0xac, "减速倒计时")

    butter_cd: int = ob.property_i32(0xb0, "黄油固定倒计时")

    is_dead: bool = ob.property_bool(0xec, '''
        是否"彻底"死亡, 即濒死时此条为False''')

    is_not_dying: bool = ob.property_bool(0xba, "不在濒死状态时为True")

    @property
    def master_id(self) -> ob.ObjId:
        """舞王id"""
        return ob.ObjId(self.base_ptr + 0xf0, self.controller)

    @property
    def partner_ids(self) -> tuple[ob.ObjId, ob.ObjId, ob.ObjId, ob.ObjId]:
        """伴舞id"""
        return tuple(ob.ObjId(self.base_ptr + 0xf4 + i * 4, self.controller) for i in range(4))

    def __str__(self) -> str:
        return f"#{self.id.index} {self.type_.name} at row {self.row + 1}"


class ZombieList(ob.obj_list(Zombie)):
    def izombie_place_zombie(self, row: int, col: int, type_: ZombieType):
        ret_idx = self.next_index
        p_challenge = self.controller.read_i32([0x6a9ec0, 0x768, 0x160])
        code = f'''
            push edx;
            mov eax, {row};
            push {col};
            push {int(type_)};
            mov ecx, {p_challenge};
            mov edx, 0x42a0f0;
            call edx;
            pop edx;
            ret;'''
        asm.run(code, self.controller)
        return self.at(ret_idx)


def get_zombie_list(ctler: Controller) -> ZombieList:
    if (t := ctler.read_i32([0x6a9ec0, 0x768])) is None:
        raise RuntimeError("game base ptr not found")
    else:
        return ZombieList(t + 0x90, ctler)
