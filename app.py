# encoding:utf-8

import os
import signal
import sys
import time

from channel import channel_factory
from common import const
from config import load_config
from plugins import *
import threading


def sigterm_handler_wrap(_signo):
    old_handler = signal.getsignal(_signo)

    def func(_signo, _stack_frame):
        logger.info("signal {} received, exiting...".format(_signo))
        conf().save_user_datas()
        if callable(old_handler):  #  check old_handler
            return old_handler(_signo, _stack_frame)
        sys.exit(0)

    signal.signal(_signo, func)


def start_channel(channel_name: str):
    channel = channel_factory.create_channel(channel_name)
    if channel_name in ["wx", "wxy", "terminal", "wechatmp","web", "wechatmp_service", "wechatcom_app", "wework",
                        const.FEISHU, const.DINGTALK, const.WECHATFERRY]:
        PluginManager().load_plugins()

    if conf().get("use_linkai"):
        try:
            from common import linkai_client
            threading.Thread(target=linkai_client.start, args=(channel,)).start()
        except Exception as e:
            pass
    channel.startup()


def run():
    try:
        # load config
        load_config()
        # ctrl + c
        sigterm_handler_wrap(signal.SIGINT)
        # kill signal
        sigterm_handler_wrap(signal.SIGTERM)

        # create channel
        channel_name = conf().get("channel_type", "wx")

        if "--cmd" in sys.argv:
            channel_name = "terminal"

        if channel_name == "wxy":
            os.environ["WECHATY_LOG"] = "warn"

        start_channel(channel_name)

        while True:
            time.sleep(1)
    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)
def siliconflow_test():

    from openai import OpenAI
    # load_config()
    print("begin")
    t1 = time.time()
    client = OpenAI(api_key="sk-41S3S2kLc3XjZwQjZho4HcSr6HOcAXteZfP4bFG9y3Emkpf6",
                    base_url="https://chat.cloudapi.vip/v1")
    response = client.chat.completions.create(
        # model='Pro/deepseek-ai/DeepSeek-R1',
        model="claude-3-7-sonnet-20250219",
        messages=[
            {"role": "system", "content": "你是一个机器人"},
            {'role': 'user',
             'content': "你好"}
        ]
    )

    t2 = time.time()
    print(f"time = {str(t2-t1)}")
    res_content = response.choices[0].message.content
    print(res_content)

    # for chunk in response:
    #     if not chunk.choices:
    #         continue
    #     if chunk.choices[0].delta.content:
    #         print(chunk.choices[0].delta.content, end="", flush=True)
    #     if chunk.choices[0].delta.reasoning_content:
    #         print(chunk.choices[0].delta.reasoning_content, end="", flush=True)

if __name__ == "__main__":
    # siliconflow_test()
    run()
