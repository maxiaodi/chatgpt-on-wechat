

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
