import requests
import demjson
import re
from prettytable import PrettyTable
import datetime
# 使用BeautifulSoup解析网页
from bs4 import BeautifulSoup

invoke_url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=fb&ft=ct&rs=&gs=0&sc=zzf&st=desc&pi=1&pn=5000"
headers = {
    'Host': 'fund.eastmoney.com',
    'Referer': 'http://fund.eastmoney.com/data/fbsfundranking.html'
}

# 获取基金简称信息
def query_etf_brief(code):
    url = "http://quote.eastmoney.com/{}.html"
    if code.startswith("5"):
        url = url.format("sh" + code)
    if code.startswith("1"):
        url = url.format("sz" + code)

    resp = requests.get(url).text
    soup = BeautifulSoup(resp, 'lxml')
    brief_name = soup.find("span", class_="quote_title_0")
    return brief_name.get_text()

# 查询ETF变动信息
def query_etf_rate_info():
    response = requests.get(invoke_url, headers=headers)
    body_data = response.text.replace("var rankData = ", "").replace(";", "")
    resp_body = demjson.decode(body_data)
    json_data = resp_body["datas"]

    head_list = ["code", "name", "alias", "fund_type"]

    tb = PrettyTable()  # 生成表格对象
    tb.field_names = head_list  # 定义表头
    pat = re.compile(r'[\u4e00-\u9fa5]+')
    etf_list = []
    for node in json_data:
        node = node[0:-1]
        arr = node.split(",")
        code = arr[0]
        name = arr[1]
        fund_type = arr[len(arr) - 1]
        result = pat.findall(fund_type)
        if len(result) == 0:
            fund_type = arr[len(arr) - 2]
        print("code {} name {} type {}".format(code, name, fund_type))
        alias = query_etf_brief(code)
        tmp_list = []
        tmp_list.append(code)
        tmp_list.append(name)
        tmp_list.append(alias)
        tmp_list.append(fund_type)
        tb.add_row(tmp_list)
        etf_list.append(tmp_list)

    print(tb)
    return etf_list


if __name__ == '__main__':
    print("start etf analyze !")
    query_etf_rate_info()
