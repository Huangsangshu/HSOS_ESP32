# 主菜单页面：顶部应用按钮 + TF 卡文件列表（点击运行卡内 .py 程序）
import time

import lvgl as lv
import machine

import sdcard
import state
import ui
from screens import calendar, setting

# TF 卡文件列表区域布局（屏幕 320x240）
_TF_AREA_X = 10
_TF_AREA_Y = 100
_TF_AREA_W = 300
_TF_AREA_H = 130
_TF_BTN_H = 30
_TF_BTN_GAP = 4
_TF_NAME_MAX = 16  # 文件名超长截断长度


def build_mainmenu():
    state.scr_mainmenu = lv.obj()
    state.scr_mainmenu.set_style_bg_color(state.BACK, 0)

    state.obj_menuclock = ui.os_show_small_clock(state.scr_mainmenu)

    obj_menubtn01 = lv.button(state.scr_mainmenu)
    obj_menubtn01.add_style(state.sty_text14, 0)
    obj_menubtn01.set_size(145, 70)
    obj_menubtn01.set_pos(10, 20)
    obj_menubtn01_text = lv.label(obj_menubtn01)
    obj_menubtn01_text.set_text("设置")
    obj_menubtn01_text.center()
    obj_menubtn01.add_event_cb(setting.goto_setting, lv.EVENT.CLICKED, None)

    obj_menubtn02 = lv.button(state.scr_mainmenu)
    obj_menubtn02.add_style(state.sty_text14, 0)
    obj_menubtn02.set_size(145, 70)
    obj_menubtn02.set_pos(165, 20)
    obj_menubtn02_text = lv.label(obj_menubtn02)
    obj_menubtn02_text.set_text("日历")
    obj_menubtn02_text.center()
    obj_menubtn02.add_event_cb(calendar.goto_calendar, lv.EVENT.CLICKED, None)

    # TF 卡文件列表（可滚动，点击运行）
    _build_tf_list(state.scr_mainmenu)


def _build_tf_list(scr):
    """在菜单下方构建 TF 卡 .py 文件滚动列表"""
    cont = lv.obj(scr)
    cont.set_size(_TF_AREA_W, _TF_AREA_H)
    cont.set_pos(_TF_AREA_X, _TF_AREA_Y)
    cont.set_style_bg_color(lv.color_make(255, 255, 180), 0)
    cont.set_style_pad_all(4, 0)
    try:
        cont.add_flag(lv.obj.FLAG.SCROLLABLE)
        cont.set_scroll_dir(lv.DIR.VER)
    except Exception:
        pass  # 滚动为增强能力，不支持时至少前几项可见

    st, files = sdcard.get_sd_state()
    if st == "NO_CARD":
        lab = lv.label(cont)
        lab.add_style(state.sty_text14, 0)
        lab.set_text("未检测到 TF 卡")
        lab.center()
        return
    if st == "NO_FILES":
        lab = lv.label(cont)
        lab.add_style(state.sty_text14, 0)
        lab.set_text("TF 卡内无脚本")
        lab.center()
        return

    y = 4
    for fn in files:
        btn = lv.button(cont)
        btn.add_style(state.sty_text14, 0)
        btn.set_size(_TF_AREA_W - 8, _TF_BTN_H)
        btn.set_pos(4, y)
        path = "/sd/" + fn
        title = sdcard.get_script_title(path)
        name = title if title else fn
        if len(name) > _TF_NAME_MAX:
            name = name[:_TF_NAME_MAX] + ".."
        lab = lv.label(btn)
        lab.set_text(name)
        lab.center()
        btn.add_event_cb(lambda e, p=path: _run_tf_file(p), lv.EVENT.CLICKED, None)
        y += _TF_BTN_H + _TF_BTN_GAP


def _run_tf_file(path):
    """在提示页中运行 TF 卡脚本，结束后返回主菜单"""
    name = path.rsplit("/", 1)[-1]

    scr = lv.obj()
    scr.set_style_bg_color(state.BACK, 0)
    lab = lv.label(scr)
    lab.add_style(state.sty_text14, 0)
    lab.set_text("运行 " + name + " ...")
    lab.center()
    lv.screen_load(scr)

    try:
        import sys

        if "/sd" not in sys.path:
            sys.path.append("/sd")
        with open(path, "r") as f:
            src = f.read()
        exec(src, {"__name__": "__main__"})
    except Exception as err:
        print("TF script error:", err)
        lab.set_text("错误: " + str(err))
        time.sleep(1.5)
    finally:
        lv.screen_load(state.scr_mainmenu)
        state.screen_state = "MAINMENU"
