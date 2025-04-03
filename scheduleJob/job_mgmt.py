# -*- coding: utf-8 -*-

import time
from datetime import datetime, time as dt_time
from typing import Any, Callable

import schedule

from bridge.reply import Reply, ReplyType
from config import conf
from stock.stock_data import SocketData


class Job(object):
    def __init__(self) -> None:
        pass

    def onEverySeconds(self, seconds: int, task: Callable[..., Any], *args, **kwargs) -> None:
        """
        每 seconds 秒执行
        :param seconds: 间隔，秒
        :param task: 定时执行的方法
        :return: None
        """
        schedule.every(seconds).seconds.do(task, *args, **kwargs)

    def onEveryMinutes(self, minutes: int, task: Callable[..., Any], *args, **kwargs) -> None:
        """
        每 minutes 分钟执行
        :param minutes: 间隔，分钟
        :param task: 定时执行的方法
        :return: None
        """
        schedule.every(minutes).minutes.do(task, *args, **kwargs)

    def onEveryHours(self, hours: int, task: Callable[..., Any], *args, **kwargs) -> None:
        """
        每 hours 小时执行
        :param hours: 间隔，小时
        :param task: 定时执行的方法
        :return: None
        """
        schedule.every(hours).hours.do(task, *args, **kwargs)

    def onEveryDays(self, days: int, task: Callable[..., Any], *args, **kwargs) -> None:
        """
        每 days 天执行
        :param days: 间隔，天
        :param task: 定时执行的方法
        :return: None
        """
        schedule.every(days).days.do(task, *args, **kwargs)

    def onEveryTime(self, times: int, task: Callable[..., Any], *args, **kwargs) -> None:
        """
        每天定时执行
        :param times: 时间字符串列表，格式:
            - For daily jobs -> HH:MM:SS or HH:MM
            - For hourly jobs -> MM:SS or :MM
            - For minute jobs -> :SS
        :param task: 定时执行的方法
        :return: None

        例子: times=["10:30", "10:45", "11:00"]
        """
        if not isinstance(times, list):
            times = [times]

        for t in times:
            schedule.every(1).days.at(t).do(task, *args, **kwargs)

    def runPendingJobs(self) -> None:
        schedule.run_pending()

def run_job_if_valid():
    stock_code_list = conf().get("stockCode")
    get_stock_flag = conf().get("getStock")
    if is_weekday() and is_working_hours() and get_stock_flag:
        for stock_code in stock_code_list:
            socket_data = SocketData()
            now_price = socket_data.getStockData(stock_code)
            ma_5_price, ma_60_price = socket_data.getStockMa60(stock_code)
            print(now_price)
            print(ma_60_price)
            print(ma_5_price)
            reply = Reply(ReplyType.TEXT, "reply_content")

def is_weekday():
    return datetime.today().weekday() < 5  # 0-4 表示周一到周五
def is_working_hours():
    now = datetime.now().time()
    return (dt_time(9, 30) <= now <= dt_time(11, 30)) or (dt_time(13, 00) <= now <= dt_time(15, 00))


if __name__ == "__main__":
    def printStr(s):
        print(s)

    job = Job()
    stock_code = "sh601288"
    job.onEveryMinutes(5, run_job_if_valid)
    # job.onEverySeconds(1, run_job_if_valid, stock_code)

    while True:
        job.runPendingJobs()
        time.sleep(1)
