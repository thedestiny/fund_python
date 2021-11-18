from lxml import etree
import requests
from prettytable import PrettyTable
import datetime
# 使用BeautifulSoup解析网页
from bs4 import BeautifulSoup
import json


# 基金变动信息
# http://fundgz.1234567.com.cn/js/005585.js
# 基金基变动信息
# http://fund.eastmoney.com/005585.html
# 阶段涨幅 http://fundf10.eastmoney.com/jdzf_515790.html
# http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jdzf&code=515790

# http://fundf10.eastmoney.com/jndzf_515790.html
# http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jdzf&code=515790
# 季度年渡涨跌幅
# http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jdndzf&code=515790
# 年度涨跌幅
# http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=yearzf&code=515790
# 季度涨跌幅
# http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=quarterzf&code=515790


# dwjz: "1.6718" 单位净值
# fundcode: "005585" 基金代码
# gsz: "1.6725" 估算值
# gszzl: "0.04"  估算增长率
# gztime: "2021-11-17 14:09" 估算时间
# jzrq: "2021-11-16" 净值日期
# name: "银河文体娱乐混合" 基金名称

# 打印表格
def print_table(head, body):
    tb = PrettyTable()  # 生成表格对象
    tb.field_names = head  # 定义表头
    tb.add_row(body)
    print(tb)


# 获取基金基本新
def query_fund_basic(code="005585", hsFlag=False):

    resp = requests.get("http://fundgz.1234567.com.cn/js/{}.js".format(code))
    data = resp.text.replace("jsonpgz(", "").replace(");", "")
    json_body = json.loads(data)
    print(json_body)
    # http://fund.eastmoney.com/005585.html
    response = requests.get("http://fund.eastmoney.com/{}.html".format(code))
    response.encoding = "UTF-8"
    print(response.apparent_encoding)
    resp_body = response.text
    soup = BeautifulSoup(resp_body, 'lxml')
    body_list = soup.find_all("table")
    num = 0
    for nod in body_list:
        # print( str(num) + "  -> " + str(nod))
        num = num + 1
    # basic_info = body_list[1]
    # 阶段涨幅表头
    stage_head_list = ["stage_week", "stage_month", "stage_month3", "stage_month6", "stage_year", "stage_year1", "stage_year2", "stage_year3",]
    stage_list = body_list[11].find_all("tr")
    # 获取第2个是基金情况 获取第4个是hs300情况
    num = 1
    if hsFlag:
        num = 3
    tmp_list = []
    for nd in stage_list[num].find_all("td"):
        val = nd.get_text()
        if "阶段涨幅" in val or "沪深300" in val:
            continue
        tmp_list.append(val.replace("%", ""))
        # print()
    # 打印阶段幅度表格
    print("\t------阶段涨跌------")
    print_table(stage_head_list, tmp_list)

    print("\t------季度涨跌------")
    query_year_quarter(body_list[12], num)
    print("\t------年度涨跌------")
    query_year_quarter(body_list[13], num)
    # # 季度涨幅
    # stage_list = body_list[12].find_all("tr")[0].find_all("th")
    # for nd in stage_list:
    #     print(nd.get_text())
    #
    # stage_list = body_list[12].find_all("tr")[num].find_all("td")
    # for nd in stage_list:
    #     print(nd)
    #
    # print("\n------------\n")
    # # 年度涨幅
    # stage_list = body_list[13].find_all("tr")
    # for nd in stage_list:
    #     print(nd)
    # # print(basic_info)
    # tmp_list = []

    return tmp_list

# 查询季度 年度数据
def query_year_quarter(data_list, num):
    stage_list = data_list.find_all("tr")[0].find_all("th")
    head_list = []
    for nd in stage_list:
        val = nd.get_text().strip()
        val = val.replace("季度", "").replace("年度", "").replace("年", "-")
        if val:
            # print(nd.get_text())
           head_list.append(val)

    body_list = []
    stage_list = data_list.find_all("tr")[num].find_all("td")
    for nd in stage_list:
        val = nd.get_text()
        if "阶段涨幅" in val or "沪深300" in val:
            continue
        body_list.append(val.replace("%", ""))

    # 打印表格
    print_table(head_list, body_list)



if __name__ == '__main__':
    print("start analyze !")
    code_list = ["005585", "000362", "008412", "008413", "009106", "009107", "007107", "007108"]
    # 基金代码 基金名称 基金公司 基金经理 创建时间 基金份额 基金类型 业绩基准 跟踪标的
    head_list = ["code", "name", "company", "manager", "create_time", "fund_share", "fund_type", "comp_basic",
                 "idx_target"]
    query_fund_basic("005585")
    #  tb = PrettyTable()  # 生成表格对象
    # tb.field_names = head_list  # 定义表头
    # for node in code_list:
        # tb.add_row(query_fund_basic(node))
        # query_fund_basic(node)
    # 输出表格
    # print(tb)
    # reslt = str(tb).replace("+", "|")
#  print(reslt)
