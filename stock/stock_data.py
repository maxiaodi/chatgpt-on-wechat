import json

from stock import easyquotation
from stock.easyquotation import sina_new


class SocketData():
    def __init__(self):
        super().__init__()
        pass

    def check_multiple_city_ids(self, city):
        pass

    def getStockData(self, stock_code='sh601288'):
        # 获取股票数据
        # 获取60日均线数据，当前股票价格低于60日均线数据发送消息
        # 获取5日均线数据，当前股票价格低于5日均线数据，发送消息
        # http://image.sinajs.cn/newchart/daily/n/sh601288.gif  股票图
        # 计算60日均线
        # http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sh601288&scale=240&ma=30&datalen=60

        quotation = easyquotation.use('sina')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
        # quotation.market_snapshot(prefix=True)

        data = quotation.real([stock_code], prefix=True)
        now_price = data[stock_code]['now']
        print(data)
        return now_price
    def getStockMa60(self,stock_code = 'sh601288'):
        sina_60 = sina_new.Sina_ma_60()
        response_str = sina_60.get_stock_ma_60(stock_code)
        daily_stock_prices = json.loads(response_str)[-60:]
        ma_60_total_price = 0.0
        ma_60_total_num = 0
        ma_5_price = daily_stock_prices[-1:][0].get("ma_price5")
        for daily_stock_price in daily_stock_prices:
            stock_close = daily_stock_price["close"]
            ma_60_total_price = ma_60_total_price + float(stock_close)
            ma_60_total_num = ma_60_total_num + 1
        ma_60_price = ma_60_total_price/ma_60_total_num
        return ma_5_price, ma_60_price

if __name__ == "__main__":
    socketData = SocketData()
    now_price = socketData.getStockData()
    ma_5_price, ma_60_price = socketData.getStockMa60()
    print(now_price)
    print(ma_60_price)
    print(ma_5_price)
