import stock_info.stock_k_line as st_line
import datetime as dt


# 处理股票代码
def handle_stock(node):
    """
    均线选股策略
    :param node:  股票代码
    :return:  返回选择结果 1 选中 0 未选
    """
    arr = node.split("\t")
    # 查询股票代码 pandas 数据
    data = st_line.query_stock_info(arr[0])
    # 计算最近三天是否符合情况
    for i in range(3):
        res = handle_data(data)
        if res == 0:
            data = data.drop(data.index.size - 1)
        else:
            return 1
    return 0



def handle_data(data):
    # 获取其日期 收盘价 均线和交易量数据 以及涨跌幅
    handle = data[["Date", "Close", "ma5", "ma10", "ma20", "Amount", "Rate"]]
    hand_srt = handle.sort_values("Date", ascending=False)
    # hand_srt["Close"] = hand_srt["Close"].apply(lambda x: round(x, 3))
    # 定义总数 上涨数量 下跌数量
    total, up, down = 0, 0, 0
    # 数据总数量
    siz = hand_srt.index.size
    # 最近 1、3、5 天的平均交易量 mean skipna 跳过nan 值
    # amt1 = handle['Amount'].iloc[siz - 1]
    # amt3 = handle['Amount'].iloc[siz - 3:].mean(skipna=True)
    amt5 = handle['Amount'].iloc[siz - 5:].mean(skipna=True)
    amt20 = handle['Amount'].iloc[siz - 20: siz - 5].mean(skipna=True)
    # 最近1天 5天 20天交易均价
    close1 = handle['Close'].iloc[siz - 1]
    close5 = handle['Close'].iloc[siz - 5: siz - 1].mean(skipna=True)
    close20 = handle['Close'].iloc[siz - 20: siz - 5].mean(skipna=True)
    # 最近两个交易日的涨跌幅
    rate = handle["Rate"].iloc[siz - 2:].mean(skipna=True)

    # 循环股票代码，按照交易日循环，只获取最近 20个交易日数据
    for idx in hand_srt.index:
        ele = handle.iloc[idx]
        if ele["Close"] > ele["ma20"]:
            up = up + 1
        else:
            down = down + 1
        total = total + 1
        if total >= 20:
            break
    # 80% 的k线在 20日均线之上 且交易量逐渐放大 且 收盘价格逐步上台阶 amt1 > amt3 and  amt1 > amt5 and
    if up / total >= 0.7 and (amt5 > amt20) \
            and (close1 > close5 and close5 > close20) and rate > 0:
        return 1
    else:
        return 0




if __name__ == '__main__':

    handle_stock("603628	清源股份")
    print("start find ma20 stock strategy ! ")
    res_list = []
    # 记录开始时间
    start = dt.datetime.now()
    st_str = dt.datetime.strftime(start, "%Y-%m-%d %H:%M:%S")
    print(st_str)
    # 加载所有的股票代码列表
    with open("./stock_list.txt", encoding="utf8", mode="r") as f:
        code_list = f.readlines()
        for node in code_list:
            try:
                res = handle_stock(node)
                if res == 1:
                    res_list.append(node)
            except Exception as e:
                print("error ", node, e)
    # 记录结束时间
    end = dt.datetime.now()
    st_str = dt.datetime.strftime(end, "%Y-%m-%d %H:%M:%S")
    # 文件名称
    file_name = dt.datetime.strftime(dt.datetime.now(), "%Y%m%d%H%M%S")
    # 写入寻找到的代码，并打印结果
    with open("./{}.txt".format(file_name), encoding="utf8", mode="a+") as f:
        for ele in res_list:
            f.write(ele)
            print(ele)
