import requests
import json
import demjson
from prettytable import PrettyTable


# 组装参数
def compose_params(code, start = "20200101"):
    tmp = ""
    if code.startswith("6"):
        tmp = "1." + code
    else:
        tmp = "0." + code

    prms = {
        "secid": tmp,
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "klt": "101",
        "fqt": "1",
        "beg": start,
        "end": "20500101",
        "lmt": "1000000",
    }
    result = ""
    for key, val in prms.items():
        result = result + key + "=" + val + "&"
    result = result[:-1]
    print(result)
    return result


# 查询数据
def query_k_line(code, start = "20200101"):
    params = compose_params(code, start)
    server = "http://54.push2his.eastmoney.com/api/qt/stock/kline/get"
    url = server + "?" + params
    resp = requests.get(url).text
    json_body = json.loads(resp)
    # 解析数据结果可以得到k线数据在 data-kline节点下
    json_data = json_body["data"]
    kline_data = json_data["klines"]
    # 创建一个对象 PrettyTable 用于打印输出结果
    bt = PrettyTable()
    title_list = ["时间", "开盘", "收盘", "最高", "最低", "成交量", "成交额", "振幅", "涨跌幅", "涨跌额", "换手率"]
    bt.field_names = title_list
    for node in kline_data:
        arr = node.split(",")
        # 将表格内容放置在 bt 中
        bt.add_row(arr)

    print(bt)
    print(kline_data)

    return kline_data


if __name__ == '__main__':
    print("start capture !")
    query_k_line("600690")
