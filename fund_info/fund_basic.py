# https://www.cnblogs.com/mxjhaima/p/13775844.html
# https://www.cnblogs.com/mxjhaima/p/13775844.html
# https://blog.csdn.net/weixin_43930694/article/details/90142678
from lxml import etree
import requests
from prettytable import PrettyTable
import datetime
# 使用BeautifulSoup解析网页
from bs4 import BeautifulSoup
import db_executor as executor
import re

# python 标准解析 "html.parser"
# lxml html 解析器 lxml
# lxml xml 解析器  lxm-xml
# html5lib 解析器  html5lib

# pip install lxml
# pip install html5lib
# pip install beautifulsoup4

# 获取基金基本新
def query_fund_basic(code):
    # http://fundf10.eastmoney.com/jbgk_005585.html
    response = requests.get("http://fundf10.eastmoney.com/jbgk_{}.html".format(code))
    resp_body = response.text
    soup = BeautifulSoup(resp_body, 'lxml')
    body_list = soup.find_all("table")
    basic_info = body_list[1]
    # print(basic_info)
    tr_list = basic_info.find_all("td")
    tmp_list = []
    # num = 0
    # for node in tr_list:
    #     val = node.get_text()
    #     print(str(num) + "  " + val)
    #
    #     num = num + 1
    # 0 code
    tmp_list.append(code)
    # 1 名称
    tmp_list.append(tr_list[1].get_text())
    # 2 基金公司
    tmp_list.append(tr_list[8].get_text())
    # 3 基金经理
    tmp_list.append(tr_list[10].get_text())

    create_time = tr_list[5].get_text().split("/")[0].strip()\
        .replace("年", "").replace("月", "").replace("日", "")
    # 4 创建时间
    tmp_list.append(create_time)
    # 5 份额
    tmp_list.append(tr_list[5].get_text().split("/")[1].strip().replace("亿份", "").replace("--", ""))
    # 6 基金类型
    tmp_list.append(tr_list[3].get_text())
    # 7 业绩基准
    tmp_list.append(tr_list[18].get_text())
    # 8 跟踪标的
    tmp_list.append(tr_list[19].get_text().replace("该基金无跟踪标的", ""))
    # print(tmp_list)
    return tmp_list


def update_fund_basic():
    fund_list = executor.query_fund_list()
    for code in fund_list:
        result = query_fund_basic(code)
        print(result)



if __name__ == '__main__':
    print("start analyze !")
    update_fund_basic()
    # code_list = ["005585", "000362", "008412", "008413", "009106", "009107", "007107", "007108"]
    # # 基金代码 基金名称 基金公司 基金经理 创建时间 基金份额 基金类型 业绩基准 跟踪标的
    # head_list = ["code", "name", "company", "manager", "create_time", "fund_share", "fund_type", "comp_basic", "idx_target"]
    #
    # tb = PrettyTable()  # 生成表格对象
    # tb.field_names = head_list  # 定义表头
    # for node in code_list:
    #    tb.add_row(query_fund_basic(node))
    # # 输出表格
    # print(tb)
    # reslt = str(tb).replace("+", "|")
    # print(reslt)



