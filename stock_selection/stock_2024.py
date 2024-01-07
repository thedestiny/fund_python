import stock_info.stock_k_line as st_line
import datetime as dt


def handle_stock(node):
    arr = node.split("\t")
    data = st_line.query_stock_info(arr[0])
    handle = data[["Date", "Close", "ma5", "ma10", "ma20", "Amount"]]
    hand_srt = handle.sort_values("Date", ascending=False)
    # hand_srt["Close"] = hand_srt["Close"].apply(lambda x: round(x, 3))
    # print(data)
    total = 0
    up = 0
    down = 0
    # 数据总数量
    siz = hand_srt.index.size
    # 最近 1、3、5 天的平均交易量 mean skipna 跳过nan 值
    amt1 = handle['Amount'].iloc[siz - 1]
    amt3 = handle['Amount'].iloc[siz - 3:].mean(skipna=True)
    amt5 = handle['Amount'].iloc[siz - 5:].mean(skipna=True)

    for idx in hand_srt.index:
        ele = handle.iloc[idx]
        if ele["Close"] > ele["ma20"]:
            up = up + 1
        else:
            down = down + 1
        total = total + 1
        if total >= 20:
            break
    # 80% 的k线在 20日均线之上 且交易量逐渐放大
    if up / total >= 0.8 and (amt1 > amt3 and amt3 > amt5):
        return 1
    else:
        return 0


if __name__ == '__main__':

    print("start app! ")
    res_list = []
    start = dt.datetime.now()
    st_str = dt.datetime.strftime(start, "%Y-%m-%d %H:%M:%S")
    print(st_str)
    with open("./stock_list.txt", encoding="utf8", mode="r") as f:
        code_list = f.readlines()
        for node in code_list:
            try:
                res = handle_stock(node)
                if res == 1:
                    res_list.append(node)
            except:
                print("error ", node)
    end = dt.datetime.now()
    st_str = dt.datetime.strftime(end, "%Y-%m-%d %H:%M:%S")
    file_name = dt.datetime.strftime(dt.datetime.now(), "%Y%m%d%H%M%S")
    print(st_str)
    with open("./{}.txt".format(file_name), encoding="utf8", mode="a+") as f:
        for ele in res_list:
            f.write(ele)
            print(ele)
