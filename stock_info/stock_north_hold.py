import requests
import json
import demjson
from prettytable import PrettyTable


# 组装参数
def compose_params(code):
    prm = "(SECURITY_CODE=" + code + ")(TRADE_DATE>='2021-10-29')"
    prms = {
        "sortColumns": "TRADE_DATE",
        "sortTypes": "-1",
        "pageSize": "100",
        "pageNumber": "1",
        "reportName": "RPT_MUTUAL_HOLDSTOCKNORTH_STA",
        "columns": "ALL",
        "filter": prm,
    }
    result = ""
    for key, val in prms.items():
        result = result + key + "=" + val + "&"
    result = result[:-1]
    print(result)
    return result


# 查询数据
def query_north_hold_detail(code):
    params = compose_params(code)
    server = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    url = server + "?" + params
    resp = requests.get(url).text
    json_body = json.loads(resp)
    # 解析数据结果可以得到k线数据在 result-data 节点下
    json_result = json_body["result"]
    data_list = json_result["data"]
    # 创建一个对象 PrettyTable 用于打印输出结果
    bt = PrettyTable()
    title_list = ["日期", "代码", "名称", "价格", "涨跌幅", "持股数", "持股市值", "持股比例", "近1日市值变化", "近5日市值变化", "近10日市值变化"]
    bt.field_names = title_list
    rate_list = []
    for node in data_list:
        date = node["TRADE_DATE"].replace(" 00:00:00", "")
        code = node["SECURITY_CODE"]
        name = node["SECURITY_NAME"]
        price = node["CLOSE_PRICE"]
        rate = round(node["CHANGE_RATE"], 2)
        share = cal_num(node["HOLD_SHARES"])
        cap = cal_num(node["HOLD_MARKET_CAP"])
        ratio = node["A_SHARES_RATIO"]
        chg1 = cal_num(node["HOLD_MARKETCAP_CHG1"])
        chg5 = cal_num(node["HOLD_MARKETCAP_CHG5"])
        chg10 = cal_num(node["HOLD_MARKETCAP_CHG10"])

        rate_list.append(ratio)
        arr = [date, code, name, price, rate, share, cap, ratio, chg1, chg5, chg10]
        # # 将表格内容放置在 bt 中
        bt.add_row(arr)

    diff = cal_model(rate_list)
    print("diff is ", diff)

    print(bt)


def cal_model(rate_list):
    if len(rate_list) > 22:
        cur_node = rate_list[0]
        pre_node = rate_list[22]
        return cur_node - pre_node
    return -100

def cal_num(num):
    if abs(num / 100000000) > 0:
        return str(round(num / 100000000, 3)) + "亿"
    else:
        return str(round(num / 10000, 3)) + "万"


if __name__ == '__main__':
    print("start capture !")
    query_north_hold_detail("600690")
