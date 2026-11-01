# 主屏页面：大时钟 + 星期 + 日期
import lvgl as lv

import state
import ui


def build_mainscreen():
    state.scr_mainscreen = lv.obj()
    state.scr_mainscreen.set_style_bg_color(state.BACK, 0)

    style_mainclock = lv.style_t()
    style_mainclock.init()
    style_mainclock.set_text_font(state.FONT48)
    style_mainclock.set_text_color(state.FRONT)

    state.obj_mainclock = lv.label(state.scr_mainscreen)
    state.obj_mainclock.add_style(style_mainclock, 0)
    state.obj_mainclock.set_pos(40, 70)

    state.obj_mainweekday = lv.label(state.scr_mainscreen)
    state.obj_mainweekday.add_style(state.sty_text14, 0)
    state.obj_mainweekday.set_pos(40, 180)

    state.obj_maindate = lv.label(state.scr_mainscreen)
    state.obj_maindate.add_style(state.sty_text14, 0)
    state.obj_maindate.set_pos(145, 180)

    state.obj_smallclock = None

    ui.os_update_clock_labels()
