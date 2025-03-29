import plugins
import requests
import re
import json
from urllib.parse import urlparse
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel import channel
from common.log import logger
from plugins import *
from datetime import datetime, timedelta
import easyquotation


class SocketData():
    def __init__(self):
        super().__init__()
        pass

    def check_multiple_city_ids(self, city):
        pass

    def getStockData(self):
        quotation = easyquotation.use('sina')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
        quotation.market_snapshot(prefix=True)
        data = quotation.real(['601288', '162411'])
        data = quotation.real(['601288', '162411'])
        print(data)


if __name__ == "__main__":
    socketData = SocketData()
    socketData.getStockData()
