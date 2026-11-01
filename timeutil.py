# 纯时间计算工具
import time


def days_in_month(y, m):
    if m == 2:
        if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0:
            return 29
        return 28
    if m in (4, 6, 9, 11):
        return 30
    return 31


def compute_weekday(y, m, d, hh, mm, ss):
    ts = time.mktime((y, m, d, hh, mm, ss, 0, 0))
    return time.localtime(ts)[6]
