# 系统设置修改模块
# 所有"修改系统设置"的业务逻辑集中于此，供各界面模块调用
import machine
import time

import lvgl as lv

import state
from timeutil import compute_weekday, days_in_month


def apply_time_to_rtc(y, m, d, hh, mm, ss):
    """将时间写入 RTC 并落盘 /time.dat（带范围校验），成功返回 True"""
    if d > days_in_month(y, m):
        d = days_in_month(y, m)
    try:
        wd = compute_weekday(y, m, d, hh, mm, ss)
        machine.RTC().datetime((y, m, d, wd, hh, mm, ss, 0))
        with open(state.TIME_SAVE_FILE, 'w') as f:
            f.write("%d,%d,%d,%d,%d,%d" % (y, m, d, hh, mm, ss))
        return True
    except Exception:
        return False


def restore_saved_time():
    """开机时恢复离线保存的时间（若有）"""
    try:
        with open(state.TIME_SAVE_FILE, 'r') as f:
            data = f.read().strip()
        parts = [int(x) for x in data.split(',')]
        if len(parts) != 6:
            return
        y, m, d, hh, mm, ss = parts
        if not (2000 <= y <= 2099 and 1 <= m <= 12 and 1 <= d <= 31):
            return
        if not (0 <= hh <= 23 and 0 <= mm <= 59 and 0 <= ss <= 59):
            return
        if d > days_in_month(y, m):
            d = days_in_month(y, m)
        wd = compute_weekday(y, m, d, hh, mm, ss)
        machine.RTC().datetime((y, m, d, wd, hh, mm, ss, 0))
    except Exception:
        pass


def set_touch_enabled(enable):
    """启用/禁用触摸输入设备（息屏时关闭触摸，防止误触）"""
    indev = state.touch_indev
    if indev is None:
        return
    try:
        if enable:
            lv.indev_enable(indev)
        else:
            lv.indev_disable(indev)
    except Exception:
        pass


def set_sleep(sleeping):
    """设置息屏状态：背光开关 + 触摸开关"""
    state.issleep = bool(sleeping)
    if sleeping:
        state.display.set_backlight(0)
        set_touch_enabled(False)
    else:
        state.display.set_backlight(75)
        set_touch_enabled(True)


def os_sleep(pin):
    """HOME 键中断处理：去抖后切换息屏状态"""
    now = time.ticks_ms()
    if time.ticks_diff(now, state.last_home) > 200:
        state.last_home = now
        set_sleep(not state.issleep)


def power_off(*args):
    """关机：拉低电源使能 GPIO40"""
    acc = machine.Pin(40, machine.Pin.OUT)
    acc.value(0)
