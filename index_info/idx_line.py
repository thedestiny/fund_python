import datetime
import requests
import json
from prettytable import PrettyTable
import pandas as pd
import datetime as dt
import talib
# import stock_list_info as info
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import arrow

from functools import reduce
#  用来正常显示中文标签 Arial Unicode MS mac 系统 SimHei windows 系统
# plt.rcParams['font.sans-serif'] = ["Arial Unicode MS"]
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# 设置数据的小数位
pd.set_option('precision', 2)
pd.set_option('expand_frame_repr', False)
# mpl.rcParams['font.sans-serif'] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False
# 单位是inches
plt.rcParams['figure.figsize'] = (20.0, 8.0)

# 东方财富数据访问接口
east_server = "http://54.push2his.eastmoney.com/api/qt/stock/kline/get"


def comp_basic_params(code, start="20200101", end="20300101", klt="101"):
    """
    组装请求参数
    """
    prms = {
        "secid": code,
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
    return result


# 查询数据
# klt k 线类型 index
def query_idxk_line(code, start="20200101", end="20300101", klt="101"):
    """
    指数信息查询和板块信息查询
    """
    if code.startswith("BK"):
        code = "90." + code
    params = comp_basic_params(code, start, end, klt)
    url = east_server + "?" + params
    resp = requests.get(url).text
    json_body = json.loads(resp)
    # 解析数据结果可以得到k线数据在 data-kline节点下
    json_data = json_body["data"]
    kline_data = json_data["klines"]
    name = json_data["name"]
    code = json_data["code"]
    stock_info = "{},{}".format(code, name)
    print(stock_info)
    # 创建一个对象 PrettyTable 用于打印输出结果
    bt = PrettyTable()
    title_list = ["时间", "开盘", "收盘", "最高", "最低", "成交量", "成交额", "振幅", "涨跌幅", "涨跌额", "换手率"]
    bt.field_names = title_list
    for node in kline_data:
        arr = node.split(",")
        # 将表格内容放置在 bt 中
        bt.add_row(arr)
    # print(bt)
    # print(kline_data)
    return kline_data, stock_info


def query_basic_pd(line_list):
    date_list, open_list, close_list, high_list, low_list = [], [], [], [], []
    # 成交量 成交额
    vol_list, amt_list = [], []
    # 振幅 涨跌幅 涨跌额 换手率
    range_list, rate_list, price_chg_list, turn_list = [], [], [], []
    for node in line_list:
        arr = node.split(",")
        date_list.append(arr[0])
        open_list.append(float(arr[1]))
        close_list.append(float(arr[2]))
        high_list.append(float(arr[3]))
        low_list.append(float(arr[4]))
        vol_list.append(float(arr[5]))
        amt_list.append(float(arr[6]))
        range_list.append(float(arr[7]))
        rate_list.append(float(arr[8]))
        price_chg_list.append(float(arr[9]))
        turn_list.append(float(arr[10]))
    # 组装 dataframe 数据
    # ["时间", "开盘", "收盘", "最高", "最低", "成交量", "成交额", "振幅", "涨跌幅", "涨跌额", "换手率"]
    data = pd.DataFrame({
        "Date": date_list, "High": high_list,
        "low": low_list, "open": open_list,
        "close": close_list, "volume": vol_list,
        "amount": amt_list, "range_rate": range_list,
        "rate": rate_list, "price_chg": price_chg_list,
        "turn_rate": turn_list
    })
    # 修改列名并进行替换
    data.rename(columns={"Date": "date", "High": "high"}, inplace=True)
    data['date'] = pd.to_datetime(data['date'])
    return data
    # 数据信息
    # print(data.info())
    # 将日期列作为行索引
    # data.set_index(['date'], inplace=True)


# 查询k线数据
def query_idx_kline_pd(code, start="20200101", end="20300101", klt="101"):
    """
    查询数据线的k 线图 指数和板块
    """
    # 获取数据并进行 pandas 转换
    line_list, stock_info = query_idxk_line(code, start, end, klt)
    data = query_basic_pd(line_list)
    return data, stock_info


# 处理指数信息
def handle_index_info():
    # 获取上证指数和深证指数成交数据
    data_sh, sh_info = query_idx_kline_pd("1.000001")
    data_sz, sz_info = query_idx_kline_pd("0.399001")
    print(data_sz, sz_info)
    print(data_sh, sh_info)

    # 提取数据并重命名字段
    sh_dt = data_sh[["date", "close", "amount", "rate", "turn_rate"]]
    sh_dt.rename(columns={"close": "SH收盘", "amount": "SH成交额", "rate": "SH涨跌幅", "turn_rate": "SH换手率"}, inplace=True)
    sz_dt = data_sz[["date", "close", "amount", "rate", "turn_rate"]]
    sz_dt.rename(columns={"close": "SZ收盘", "amount": "SZ成交额", "rate": "SZ涨跌幅", "turn_rate": "SZ换手率"}, inplace=True)
    # 将上证指数和深证指数数据进行合并，并将成交额进行转换，原成交额单位是元，需要转换成亿元
    mg_data = pd.merge(sh_dt, sz_dt, how="inner", on="date")
    mg_data["SH成交额"] = mg_data["SH成交额"] / 100_000_000
    mg_data["SZ成交额"] = mg_data["SZ成交额"] / 100_000_000

    # 计算总的成交额和换手率
    mg_data["两市成交额"] = (mg_data["SH成交额"] + mg_data["SZ成交额"])
    # 两市成交总额 / (上证市值 + 深证市值)
    mg_data["两市换手"] = mg_data["两市成交额"] / (mg_data["SH成交额"] / mg_data["SH换手率"] + mg_data["SZ成交额"] / mg_data["SZ换手率"])
    # 设置数据位数
    mg_data.round({"SH收盘": 1, "SZ收盘": 1})
    # 日期转字符串，提取年份和日期
    mg_data['year'] = mg_data['date'].apply(lambda x: x.strftime('%Y%m%d')[:4])
    mg_data['date'] = mg_data['date'].apply(lambda x: x.strftime('%Y%m%d')[2:])
    # 提取需要展示IDE字段
    plot_data = mg_data[["date", "两市成交额", "两市换手"]]
    # p_dat = plot_data.set_index('date', inplace=False)
    # print(p_dat)
    # 提取22年以来的数据，结果数据过多的问题
    p_dat = plot_data[plot_data.date > "220101"]
    # 删除原有索引并且进行替换
    p_dat.reset_index(drop=True, inplace=True)
    plt.plot(p_dat["date"], p_dat["两市成交额"], color='red')
    plt.title('A股市场成交额')
    plt.xlabel('时间')
    plt.ylabel('亿元')
    plt.grid(True)
    xticks = list(range(0, len(p_dat["date"]), 30))
    las = [p_dat["date"][x] for x in xticks]
    print(las)
    labels = [str(p_dat["date"][x]) for x in xticks]
    # vertical
    plt.xticks(xticks, labels, rotation='0')
    plt.show()

    print(plot_data)

    # 简单的导出方式，不能进行单元格的设置
    # mg_data.to_excel("data-历史交易统计.xlsx", index=True, header=True, sheet_name="dt1")

    # 创建一个 excel
    writer = pd.ExcelWriter("data-历史交易统计.xlsx", engine="xlsxwriter")
    mg_data.to_excel(writer, index=False, header=True, sheet_name="dt1")
    # 设置表格 sheet
    work_sht = writer.sheets["dt1"]
    # 设置表格宽度
    work_sht.set_column("A:L", 10)
    # work_sht.set_column("B:B", 12)
    writer.save()


if __name__ == '__main__':
    print("start index capture !")
    handle_index_info()
