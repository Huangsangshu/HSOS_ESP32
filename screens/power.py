# 电源页面：关机 / 息屏
import lvgl as lv

import state
import system
import ui


def goto_power(e=None):
    state.screen_state = "POWER"
    lv.screen_load(state.scr_set_power)


def _sleep_cb(e=None):
    system.set_sleep(True)


def build_power():
    state.scr_set_power = lv.obj()
    state.scr_set_power.set_style_bg_color(state.BACK, 0)
    state.obj_powerclock = ui.os_show_small_clock(state.scr_set_power)

    obj_menubtn01 = lv.button(state.scr_set_power)
    obj_menubtn01.add_style(state.sty_text14, 0)
    obj_menubtn01.set_size(145, 70)
    obj_menubtn01.set_pos(10, 20)
    obj_menubtn01_text = lv.label(obj_menubtn01)
    obj_menubtn01_text.set_text("关机")
    obj_menubtn01_text.center()
    obj_menubtn01.add_event_cb(system.power_off, lv.EVENT.CLICKED, None)

    obj_menubtn02 = lv.button(state.scr_set_power)
    obj_menubtn02.add_style(state.sty_text14, 0)
    obj_menubtn02.set_size(145, 70)
    obj_menubtn02.set_pos(165, 20)
    obj_menubtn02_text = lv.label(obj_menubtn02)
    obj_menubtn02_text.set_text("息屏")
    obj_menubtn02_text.center()
    obj_menubtn02.add_event_cb(_sleep_cb, lv.EVENT.CLICKED, None)
