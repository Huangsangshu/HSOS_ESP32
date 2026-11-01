# 关于页面
import lvgl as lv

import state
import ui


def goto_about(e=None):
    state.screen_state = "ABOUT"
    lv.screen_load(state.scr_about)


def build_about():
    state.scr_about = lv.obj()
    state.scr_about.set_style_bg_color(state.BACK, 0)
    state.obj_aboutclock = ui.os_show_small_clock(state.scr_about)
    text = lv.label(state.scr_about)
    text.set_size(320, 220)
    text.set_pos(0, 20)
    text.add_style(state.sty_text14, 0)
    text.set_text("\n HSOS\n\n 版本号 snapshot-20261101\n\n Huangsangshu & Cookie987\n\n 该项目已于Github开源\n\n the test version \n doesn't represent the final result")
