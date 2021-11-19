import requests
import json
import demjson
from prettytable import PrettyTable
import db_executor as executor

# 数据表格的列表表头字段
title_list = ["code", "name", "value"]


# 查询基金列表信息
def query_fund_list(page=1, lx="1"):
    req_url = "http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?lx={}&sort=zdf,desc&page={},20&onlySale=0"\
        .format(lx, page)
    response = requests.get(req_url)
    # 输出响应头
    # print(response.headers)
    # 获取请求结果并替换，否则结果不能进行格式化json
    resp_body = response.text.replace("var db=", "")
    # 本来首选是这个json, 因为json 不支持 {a :"1"} 这样的转换，因此使用了 demojson
    # json_data = json.loads(resp_body)
    # 转换对象为 json 对象,使不规则的json格式化为json对象

    code_info_list = []
    resp_body = demjson.decode(resp_body)
    if not resp_body:
        return []
    # 获取结果数组
    fund_list = resp_body["datas"]
    body_list = []
    for node in fund_list:
        tmp = []
        tmp.append(node[0])
        tmp.append(node[1])
        tmp.append(node[3])
        body_list.append(tmp)
    # 创建一个对象 PrettyTable 用于打印输出结果
    bt = PrettyTable()
    # 将表头信息信息放入bt 中
    bt.field_names = title_list
    # 将表格内容放置在 bt 中
    bt.add_rows(body_list)
    # 打印结果
   #  print(bt)
    return body_list

# 保存数据列表
def update_fund_list():
    # 类型的名称
    lx_list = {"1": ""}
    for key, value in lx_list.items():
        for i in range(1, 50):
            result = query_fund_list(i, key)
            if result:
              sql_template = "INSERT INTO `tb_fund_list`(`code`, `name`, `fund_type`) VALUES ('{0}','{1}','{2}') " \
                             "on duplicate key update `code` = '{0}', `name` = '{1}' ,`fund_type` = '{2}';"
              for node in result:
                    exe_sql = sql_template.format(node[0], node[1], key)
                    executor.save_data(exe_sql)
                    # print(exe_sql)

if __name__ == "__main__":
    # 这里只打印了第一页，循环打印结果就不写了，大家都会的
    update_fund_list()
