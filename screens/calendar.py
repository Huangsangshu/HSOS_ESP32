# 日历页面
import time

import lvgl as lv

import state
import ui


def goto_calendar(e=None):
    state.screen_state = "CALENDAR"
    lv.screen_load(state.scr_calendar)


def build_calendar():
    state.scr_calendar = lv.obj()
    state.scr_calendar.set_style_bg_color(state.BACK, 0)

    state.obj_calclock = ui.os_show_small_clock(state.scr_calendar)

    cal = lv.calendar(state.scr_calendar)
    cal.set_size(320, 220)
    cal.set_pos(0, 20)
    cal.add_style(state.sty_text14, 0)
    now_time = time.localtime()
    cal.set_today_date(now_time[0], now_time[1], now_time[2])
    cal.set_shown_year(now_time[0])
    cal.set_shown_month(now_time[1])
