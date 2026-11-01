# SD 卡驱动：SDMMC 4-bit 模式初始化与挂载
# 引脚依据《触屏版二次开发文档》GPIO 分配表
import machine
import os
from machine import Pin

# SD 卡引脚定义
SD_CLK = 21
SD_CMD = 47
SD_D0 = 14
SD_D1 = 3
SD_D2 = 38
SD_D3 = 48

SD_MOUNT = "/sd"  # 挂载点


def init_sd(slot=0, width=4):
    """初始化并挂载 SD 卡。

    成功返回 True；失败打印原因并返回 False（不影响系统启动）。
    本板卡槽 SDMMC 引脚经 GPIO 矩阵自定义：CLK=21/CMD=47/D0=14/D1=3/D2=38/D3=48，
    必须显式传入（固件默认引脚 14/15/2/4/12/13 与卡槽不符，会 OSError 16）。
    data_pins 必须使用元组（定制固件按 tuple 解析，list 会读错内存导致崩溃重启）。
    freq 暂用 1MHz（已验证稳定），后续可逐步提频测试。
    """
    try:
        pins = (SD_D0, SD_D1, SD_D2, SD_D3)[:width]
        sd = machine.SDCard(
            slot=slot, width=width,
            clk=SD_CLK, cmd=SD_CMD,
            data_pins=pins,
            freq=1000000,
        )
        os.mount(sd, SD_MOUNT)
        print("SD card mounted at", SD_MOUNT)
        return True
    except Exception as err:
        print("SD card init failed:", err)
        return False


def sd_available():
    """SD 卡是否已成功挂载"""
    try:
        os.listdir(SD_MOUNT)
        return True
    except Exception:
        return False


def list_py_files():
    """返回 /sd 下所有 .py 文件名（已排序）；未挂载或无文件时返回空列表"""
    if not sd_available():
        return []
    try:
        names = [n for n in os.listdir(SD_MOUNT) if n.lower().endswith(".py")]
        names.sort()
        return names
    except Exception:
        return []


def get_sd_state():
    """区分 TF 卡状态，返回 (state, files)。

    state 取值：
      "NO_CARD"  - SD 卡未挂载（未插卡或初始化/挂载失败）
      "NO_FILES" - 已挂载，但 /sd 下没有 .py 文件
      "OK"       - 已挂载，且有 .py 文件
    files 为 /sd 下排序后的 .py 文件名列表（非 OK 状态时为空列表）。
    """
    if not sd_available():
        return "NO_CARD", []
    try:
        names = [n for n in os.listdir(SD_MOUNT) if n.lower().endswith(".py")]
        names.sort()
    except Exception:
        return "NO_CARD", []
    if not names:
        return "NO_FILES", []
    return "OK", names


def get_script_title(path):
    """读取脚本头部自定义标题（__title__ = "xxx"，支持单/双引号与行尾注释）。

    约定：脚本开头（前 20 行内）定义 __title__ 即可自定义菜单显示名称；
    未定义返回 None，由调用方回退显示文件名。
    """
    try:
        with open(path, "r") as f:
            for _ in range(20):
                line = f.readline()
                if not line:
                    break
                s = line.strip()
                if not s.startswith("__title__"):
                    continue
                eq = s.find("=")
                if eq == -1:
                    continue
                val = s[eq + 1:].strip()
                if len(val) >= 2 and val[0] in ('"', "'"):
                    q = val[0]
                    end = val.find(q, 1)
                    if end != -1:
                        return val[1:end]
    except Exception:
        pass
    return None
