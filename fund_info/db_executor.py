import pymysql

stand_db = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "pwd": "Myroot123!",
    "name": "fund_data",
}

# 标准库数据库链接
std_db = pymysql.connect(host=stand_db["host"], port=stand_db["port"], database=stand_db["name"],
                         charset="utf8", user=stand_db["user"],
                         password=stand_db["pwd"])
# 查询 fund list
def query_fund_list():
    sql = "select `code` from tb_fund_list order by id asc"
    rslt = query_data(sql)
    tmp_list = []
    for node in rslt:
        tmp_list.append(node[0])
    return tmp_list

# 查询数据
def query_data(sql):
    cursor = std_db.cursor()
    cursor.execute(sql)
    rslt = cursor.fetchall()
    cursor.close()
    return rslt

# 保存数据
def save_data(sql):
   cursor = std_db.cursor()
   cursor.execute(sql)
   cursor.close()
   std_db.commit()

if __name__ == "__main__":
    # 这里只打印了第一页，循环打印结果就不写了，大家都会的
    fund_list = query_fund_list()
    print(fund_list)