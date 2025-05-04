import requests
import json
import demjson
from prettytable import PrettyTable
import pandas as pd
import talib


# 参数请求组装
def compose_params(code, start="20200101", end="20300101", klt="101"):
    tmp = "0." + code
    if code.startswith("6") or code.startswith("5"):
        tmp = "1." + code
    prms = {
        "secid": tmp,
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "klt": klt,
        "fqt": "1",
        "beg": start,
        "end": end,
        "lmt": "1000000",
    }
    result = ""
    for key, val in prms.items():
        result = result + key + "=" + val + "&"
    result = result[:-1]
    # print(result)
    return result


# 查询数据
def query_k_line(code, start="20200101", end="20300101", klt="101"):
    params = compose_params(code, start, end, klt)
    server = "http://54.push2his.eastmoney.com/api/qt/stock/kline/get"
    url = server + "?" + params
    resp = requests.get(url).text
    json_body = json.loads(resp)
    # 解析数据结果可以得到k线数据在 data-kline节点下
    json_data = json_body["data"]
    kline_data = json_data["klines"]
    # 创建一个对象 PrettyTable 用于打印输出结果
    bt = PrettyTable()
    title_list = ["时间", "开盘", "收盘", "最高", "最低", "成交量",
                  "成交额", "振幅", "涨跌幅", "涨跌额", "换手率"]
    bt.field_names = title_list
    for node in kline_data:
        arr = node.split(",")
        # 将表格内容放置在 bt 中
        bt.add_row(arr)
    # print(bt)
    # print(kline_data)
    return kline_data












def query_stock_pandas(code, sat="20240101"):

    line_list = query_k_line(code, sat)
    date_list, open_list, close_list, high_list,\
    low_list, rate_list = [], [], [], [], [], []
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
        rate_list.append(float(arr[8]))
    # 组装 dataframe 数据
    # Date High Low Open Close Volume Amount Rate
    data = pd.DataFrame({
        "Date": date_list,
        "High": high_list,
        "Low": low_list,
        "Open": open_list,
        "Close": close_list,
        "Volume": vol_list,
        "Amount": amt_list,
        "Rate": rate_list
    })
    return data


def query_stock_info(code, sat="20211001"):
    """
    查询股票信息
    :param code:
    :param sat:
    :return:
    """

    line_list = query_k_line(code, sat)

    date_list, open_list, close_list, high_list, low_list, rate_list = [], [], [], [], [], []
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
        rate_list.append(float(arr[8]))

    # 组装 dataframe 数据
    data = pd.DataFrame({
        "Date": date_list,
        "High": high_list,
        "Low": low_list,
        "Open": open_list,
        "Close": close_list,
        "Volume": vol_list,
        "Amount": amt_list,
        "Rate": rate_list
    })

    # date_series = data['Date']
    # print(date_series)

    # 计算 macd 数据
    # talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data['Close'], fastperiod=12, slowperiod=26,
                                                                      signalperiod=9)
    # 计算均线数据
    data["ma5"] = talib.MA(data["Close"], timeperiod=5)
    data["ma7"] = talib.MA(data["Close"], timeperiod=7)
    data["ma10"] = talib.MA(data["Close"], timeperiod=10)
    data["ma20"] = talib.MA(data["Close"], timeperiod=20)
    data["ma30"] = talib.MA(data["Close"], timeperiod=30)
    data["ma60"] = talib.MA(data["Close"], timeperiod=60)
    data["ma120"] = talib.MA(data["Close"], timeperiod=120)
    data["ma250"] = talib.MA(data["Close"], timeperiod=250)

    return data


if __name__ == '__main__':
    print("start capture !")
    # todo stock
    ele = query_k_line("300059")
    print(ele)
