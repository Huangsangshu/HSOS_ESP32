# 系统启动与主循环
import time

import lvgl as lv
import machine

import hardware
import sdcard
import state
import system
import ui
from screens import about, calendar, mainmenu, mainscreen, power, setting, timeset


def os_button_pressed(pin):
    if not state.issleep:
        now = time.ticks_ms()
        if time.ticks_diff(now, state.last_boot) > 200:
            state.last_boot = now
            state.need_switch = True


def boot():
    hardware.init_display_and_touch()
    ui.init_styles()

    state.btn_boot = machine.Pin(0, machine.Pin.IN)
    state.btn_home = machine.Pin(39, machine.Pin.IN)

    # 显示开机 LOGO
    scr = lv.obj()
    scr.set_style_bg_color(state.BACK, 0)
    obj_logo = lv.label(scr)
    obj_logo.add_style(state.sty_text14, 0)
    obj_logo.set_pos(130, 100)
    obj_logo.set_text("HSOS")
    lv.screen_load(scr)

    time.sleep(2)

    state.btn_boot.irq(trigger=machine.Pin.IRQ_FALLING, handler=os_button_pressed)
    state.btn_home.irq(trigger=machine.Pin.IRQ_FALLING, handler=system.os_sleep)

    # 恢复离线保存的时间（若有）
    system.restore_saved_time()

    # 初始化外置 SD 卡（失败不影响系统启动）
    sdcard.init_sd()

    # 预构建所有页面
    mainscreen.build_mainscreen()
    mainmenu.build_mainmenu()
    calendar.build_calendar()
    setting.build_setting()
    timeset.build_timeset()
    about.build_about()
    power.build_power()

    state.screen_state = "MAINSCREEN"
    lv.screen_load(state.scr_mainscreen)

    # 主循环：仅用于硬件物理按键检查和非阻塞轮询
    last_time_refresh = 0
    while True:
        if state.need_switch:
            state.need_switch = False
            if state.screen_state in ("MAINSCREEN", "CALENDAR", "SETTING"):
                lv.screen_load(state.scr_mainmenu)
                state.screen_state = "MAINMENU"
            elif state.screen_state == "MAINMENU":
                lv.screen_load(state.scr_mainscreen)
                state.screen_state = "MAINSCREEN"
            elif state.screen_state in ("SETTIME", "ABOUT", "POWER"):
                lv.screen_load(state.scr_setting)
                state.screen_state = "SETTING"

        now_ms = time.ticks_ms()
        # 如果在时钟页面，实时更新时间
        if time.ticks_diff(now_ms, last_time_refresh) > 1000:
            last_time_refresh = now_ms
            if state.screen_state == "MAINSCREEN":
                ui.os_update_clock_labels()
            elif state.screen_state == "MAINMENU" and state.obj_menuclock:
                ui.os_update_small_clock(state.obj_menuclock)
            elif state.screen_state == "CALENDAR" and state.obj_calclock:
                ui.os_update_small_clock(state.obj_calclock)
            elif state.screen_state == "SETTING" and state.obj_setclock:
                ui.os_update_small_clock(state.obj_setclock)
            elif state.screen_state == "ABOUT" and state.obj_aboutclock:
                ui.os_update_small_clock(state.obj_aboutclock)
            elif state.screen_state == "POWER" and state.obj_aboutclock:
                ui.os_update_small_clock(state.obj_powerclock)

        time.sleep_ms(5)
