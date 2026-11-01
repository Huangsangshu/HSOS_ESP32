# 设置界面：系统设置入口列表
import lvgl as lv

import state
import ui
from screens import about, power, timeset


def goto_setting(e=None):
    state.screen_state = "SETTING"
    lv.screen_load(state.scr_setting)


def build_setting():
    state.scr_setting = lv.obj()
    state.scr_setting.set_style_bg_color(state.BACK, 0)
    state.obj_setclock = ui.os_show_small_clock(state.scr_setting)

    obj_menubtn01 = lv.button(state.scr_setting)
    obj_menubtn01.add_style(state.sty_text14, 0)
    obj_menubtn01.set_size(145, 70)
    obj_menubtn01.set_pos(10, 20)
    obj_menubtn01_text = lv.label(obj_menubtn01)
    obj_menubtn01_text.set_text("日期与时间")
    obj_menubtn01_text.center()
    obj_menubtn01.add_event_cb(timeset.open_timeset, lv.EVENT.CLICKED, None)

    obj_menubtn02 = lv.button(state.scr_setting)
    obj_menubtn02.add_style(state.sty_text14, 0)
    obj_menubtn02.set_size(145, 70)
    obj_menubtn02.set_pos(165, 20)
    obj_menubtn02_text = lv.label(obj_menubtn02)
    obj_menubtn02_text.set_text("显示")
    obj_menubtn02_text.center()
    obj_menubtn02.add_event_cb(None, lv.EVENT.CLICKED, None)

    obj_menubtn03 = lv.button(state.scr_setting)
    obj_menubtn03.add_style(state.sty_text14, 0)
    obj_menubtn03.set_size(145, 70)
    obj_menubtn03.set_pos(10, 100)
    obj_menubtn03_text = lv.label(obj_menubtn03)
    obj_menubtn03_text.set_text("电源")
    obj_menubtn03_text.center()
    obj_menubtn03.add_event_cb(power.goto_power, lv.EVENT.CLICKED, None)

    obj_menubtn04 = lv.button(state.scr_setting)
    obj_menubtn04.add_style(state.sty_text14, 0)
    obj_menubtn04.set_size(145, 70)
    obj_menubtn04.set_pos(165, 100)
    obj_menubtn04_text = lv.label(obj_menubtn04)
    obj_menubtn04_text.set_text("关于")
    obj_menubtn04_text.center()
    obj_menubtn04.add_event_cb(about.goto_about, lv.EVENT.CLICKED, None)
