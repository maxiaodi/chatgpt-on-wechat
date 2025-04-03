# coding:utf8
import re
import time
from stock.easyquotation import basequotation


class Sina_ma_60(basequotation.BaseQuotation):
    """新浪ma60日均线"""


    @property
    def stock_api(self) -> str:
        return "https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={stockCode}&scale=240&ma=5&datalen=1000"

    def _get_headers(self) -> dict:
        headers = super()._get_headers()
        return {
            **headers,
            'Referer': 'http://finance.sina.com.cn/'
        }

    def get_stock_ma_60(self, stock_code):
        headers = self._get_headers()
        url = self.stock_api.format(stockCode=stock_code)
        r = self._session.get(url, headers=headers)
        return r.text

