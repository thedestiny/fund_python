import db_executor as executor
import fund_list
import etf_rate_info
import fund_rate_info
import fund_price_info


# 处理数字
def handle(val):
    return val.strip().replace("--", '0')


# 保存数据列表
def update_fund_list():
    # 类型的名称
    lx_list = {"1": "全部"}
    # 场外基金信信息
    for key, value in lx_list.items():
        for i in range(1, 65):
            result = fund_list.query_fund_list(i, key)
            if result:
                sql_template = "INSERT INTO `tb_fund_list`(`code`, `name`, `fund_type`) VALUES ('{0}','{1}','{2}') " \
                               "on duplicate key update `code` = '{0}', `name` = '{1}' ,`fund_type` = '{2}';"
                for node in result:
                    exe_sql = sql_template.format(node[0], node[1], key)
                    executor.save_data(exe_sql)
                    # print(exe_sql)
    # ETF 基金信息
    etf_list = etf_rate_info.query_etf_rate_info()
    sql_template = "INSERT INTO `tb_fund_list`(`code`, `name`, `fund_type`, `alias`,`etf_flag`) VALUES ('{0}','{1}','{2}','{3}','{4}') " \
                   "on duplicate key update `code` = '{0}', `name` = '{1}' ,`fund_type` = '{2}',`alias` = '{3}' ,`etf_flag` = '{4}';"
    for node in etf_list:
        exe_sql = sql_template.format(node[0], node[1], node[3], node[2], "1")
        executor.save_data(exe_sql)


# 保存基金变动信息
def update_fund_rate():
    sql_template = "update tb_fund_list set stage_week = '{}', stage_month1 = '{}', stage_month3 = '{}', stage_month6 = '{}'," \
                   "stage_year = '{}',stage_year1 = '{}',stage_year2 = '{}',stage_year3 = '{}'," \
                   " format_time = '{}', price= '{}', rate_change ='{}', fund_size ='{}' where `code` = '{}';"

    sql_tmpl = """insert ignore into tb_fund_ext_list (`code`,`data_type`,`data_name`,`data_value`) values ()"""

    for node in executor.query_fund_list():
        try:
            # 基金阶段涨幅统计信息
            rate, dic_data = fund_rate_info.query_fund_basic(node)
            # 基金价格信息
            update_date, price, price_percent, fund_size = fund_price_info.query_fund_price(node)
            # 组装sql模板
            sql = sql_template.format(handle(rate[0]), handle(rate[1]), handle(rate[2]), handle(rate[3]),
                                      handle(rate[4]), handle(rate[5]), handle(rate[6]), handle(rate[7]),
                                      update_date, price, price_percent, fund_size,
                                      node)
            # 保存数据
            executor.save_data(sql)
            # 基金扩展信息
            sql2 = sql_tmpl.replace("()", "")
            if len(dic_data) > 0:
                for key, val in dic_data.items():
                    data_type = "2"
                    if "-" in key:
                        data_type = "1"
                    sql2 += "('{}','{}','{}','{}'),".format(node, data_type, key, handle(val))
                sql2 = sql2[0:-1]
                # print(sql2)
                executor.save_data(sql2)
        except:
            print("code {} error ".format(node))


if __name__ == '__main__':
    print("start update fund data!")
    # 更新基金列表信息
    update_fund_list()
    # 更新基金变动信息
    update_fund_rate()
