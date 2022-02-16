import requests
import json
import talib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.pyplot import MultipleLocator

# http://fundf10.eastmoney.com/jjjz_167301.html

req_header = {
    "Referer": "http://fundf10.eastmoney.com/"
}
# 设置中文显示问题，防止乱码
mpl.rcParams['font.sans-serif'] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False

def fund_hist_data(code, startDate="2021-01-01", endDate="2030-01-01"):
    """
    查询基金历史变动信息
    """
    req_url = "http://api.fund.eastmoney.com/f10/lsjz?fundCode={}&pageIndex=1&pageSize=1000&startDate={}&endDate={}".format(
        code, startDate, endDate)

    body_data = requests.get(req_url, headers=req_header).text
    # 数据节点在 Data.LSJZList
    json_data = json.loads(body_data)
    data_list = json_data["Data"]["LSJZList"]
    # 倒序排列数据
    data_list.reverse()
    # FSRQ 净值日期 DWJZ 单位净值 LJJZ 累计净值  JZZZL 净值增长率
    time_list = []
    value_list = []
    for node in data_list:
        time_list.append(node["FSRQ"])
        value_list.append(round(float(node["DWJZ"]), 5))

    return time_list, value_list


def fund_plot_data(code):
    """
    基金净值走势图
    """
    time_list, value_list = fund_hist_data(code)
    data = pd.DataFrame({"close": value_list})

    data["ma5"] = talib.MA(data["close"], timeperiod=5)
    data["ma7"] = talib.MA(data["close"], timeperiod=7)
    data["ma10"] = talib.MA(data["close"], timeperiod=10)
    data["ma20"] = talib.MA(data["close"], timeperiod=20)

    plt.figure(figsize=(15, 5))  # 定义一个图像窗口
    plt.title(u'基金净值走势图')
    plt.xlabel(u'时间')
    plt.ylabel(u'净值')
    # 收盘价 5日 7日 10日 20日净值均线
    plt.plot(time_list, data["close"].to_list(), label='value')
    plt.plot(time_list, data["ma5"].to_list(), label="ma5")
    plt.plot(time_list, data["ma7"].to_list(), label="ma7")
    plt.plot(time_list, data["ma10"].to_list(), label="ma10")
    plt.plot(time_list, data["ma20"].to_list(), label="ma20")

    # ax为两条坐标轴的实例
    ax = plt.gca()
    # 把x轴的刻度间隔设置为1，并存在变量里
    x_major_locator = MultipleLocator(20)
    # 把x轴的主刻度设置为1的倍数
    ax.xaxis.set_major_locator(x_major_locator)

    # 显示网格和图例
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == '__main__':
    fund_plot_data("167301")
