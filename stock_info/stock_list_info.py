import requests
import json

# stock 列表信息查询
stock_list_api = "https://78.push2.eastmoney.com/api/qt/clist/get"
# stock 财务数据基本信息
stock_basic_api = "http://push2.eastmoney.com/api/qt/stock/get"



# 参数请求组装
def compose_list_params():
    prms = {
        "pn": "1",
        "pz": "5000",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048",
        # "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "po": "1",
        "np": "1",
    }
    result = ""
    for key, val in prms.items():
        result = result + key + "=" + val + "&"
    result = result[:-1]
    print(result)
    return result

# 参数请求组装

def compose_basic_params(code):
    # 上海市场前缀使用 1. 深圳市场为 0.
    secid = "0." + code
    if code.startswith("6"):
        secid = "1." + code
    prms = {

        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048",
        "fields": "f57,f58,f62,f55,f162,f92,f167,f183,f184,f105,f185,f186,f187,f173,f188,f84,f116,f85,f117,f190,f189,f86",
        "fltt": "2",
        "invt": "2",
        "secid": secid
    }
    result = ""
    for key, val in prms.items():
        result = result + key + "=" + val + "&"
    result = result[:-1]
    print(result)
    return result


# 股票代码列表 https://quote.eastmoney.com/center/gridlist.html
# 数据接口列表 https://78.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152
def query_stock_list():
    """
    查询stock list
    :return:
    """
    req_url = stock_list_api + "?" + compose_list_params()
    body = requests.get(req_url).text
    json_body = json.loads(body)
    total_num = json_body["data"]["total"]
    data_list = json_body["data"]["diff"]
    print("total num {}".format(total_num))
    for node in data_list:
        # 代码和名称
        code, name = node["f12"], node["f14"]
        print(code, name)

def stock_basic_info(code):
    """
    获取 stock 基本信息 财务数据
    :param code:
    :return:
    """
    # http://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=
    # f57,f58,f62,f55,f162,f92,f167,f183,f184,f105,f185,f186,f187,f173,f188,f84,f116,f85,f117,f190,f189,f86&secid=0.300949
    req_url = stock_basic_api + "?" + compose_basic_params(code)
    body = requests.get(req_url).text
    json_body = json.loads(body)
    data_node = json_body["data"]
    print(data_node)




    pass

if __name__ == '__main__':
    print("start capture !")
    # query_stock_list()
    stock_basic_info("603158")
