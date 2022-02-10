import backtrader as bt
from backtrader.feeds import PandasData
import datetime
import pandas as pd
import stock_info.stock_k_line as kline

if __name__ == '__main__':
    data1 = set(["12"])
    data2 = set(["12", "45", "67"])

    line_list = kline.query_k_line("600690", "20210101")

    date_list, open_list, close_list, high_list, low_list = [], [], [], [], []
    # 成交量 成交额
    vol_list, amt_list = [], []

    for node in line_list:
        arr = node.split(",")
        date_list.append(arr[0])
        open_list.append(float(arr[1]))
        close_list.append(float(arr[2]))
        high_list.append(float(arr[3]))
        low_list.append(float(arr[4]))
        vol_list.append(float(arr[5]))
        amt_list.append(float(arr[6]))

    # 组装 dataframe 数据
    data = pd.DataFrame({
        "Date": date_list,
        "High": high_list,
        "Low": low_list,
        "Open": open_list,
        "Close": close_list,
        "Volume": vol_list,
        "Amount": amt_list
    })

    data["Date"] = pd.to_datetime(data["Date"])
    # 修改列名并进行替换
    data.rename(
        columns={"Date": "date", "High": "high", "Low": "low", "Close": "close", "Open": "open", "Volume": "volume",
                 "Amount": "amount"},
        inplace=True)
    # 添加列
    data["openinterest"] = 0.0
    # 设置日期为索引
    data.set_index(keys=['date'], inplace=True)
    print(data.head(4))
    # 删除字段
    data.drop(["amount"], inplace=True, axis=1)
    print(data.head(4))
    print(data.info())

    bt.feeds.PandasDirectData(dataname=data,
                              # datatime = 1,
                              open=3,
                              high=1,
                              low=2,
                              close=4,
                              volume=5,
                              openinterest=-1,
                              fromdate= datetime(2021, 1, 1),
                              todate= datetime(2022, 2, 2)
                              )

    title_list = ["时间", "开盘", "收盘", "最高", "最低", "成交量", "成交额", "振幅", "涨跌幅", "涨跌额", "换手率"]
    print(data2 - data1)
    kdata = {}
    cerebro = bt.Cerebro()
    for secu in set(kdata.keys()) - set(['benchmark']):
        # 数据列和数据的日期
        df = PandasData(dataname=kdata[secu], fromdate=kdata[secu].index[0], todate=kdata[secu].index[-1])
        cerebro.adddata(df, name=secu)

        # 加载数据到模型中
    data = bt.feeds.GenericCSVData(
        dataname='600519.csv',
        fromdate=datetime.datetime(2010, 1, 1),
        todate=datetime.datetime(2020, 4, 12),
        dtformat='%Y%m%d',
        datetime=2,
        open=3,
        high=4,
        low=5,
        close=6,
        volume=10
    )

    print(data)
