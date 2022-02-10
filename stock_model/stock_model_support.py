import stock_info.stock_k_line as kline
import matplotlib.pyplot as plt
import pandas as pd
import talib
from matplotlib.pyplot import MultipleLocator
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False
# 单位是inches
plt.rcParams['figure.figsize'] = (20.0, 8.0)


#
def find_support_model(date_list, m5_list, m10_list, m20_list, close_list, result_flag=1):
    # 日期 5日线 10日线 20日线 收盘价 价托 1 上涨 -1 下跌
    # 设置变量
    ll_num = len(date_list)
    cnt, last_stage, stage_cnt = 0, 0, 0
    point1_val, point2_val, point3_val = {}, {}, {}

    for date, m5, m10, m20 in zip(date_list, m5_list, m10_list, m20_list):
        if cnt > ll_num - 2:
            break
        # 排除不符合条件的数据 数据不能为 None
        if m5 > 0 and m10 > 0 and m20 > 0:
            # 寻找第一个点 5日线上穿10日线
            if last_stage == 0:
                m5_next, m10_next = m5_list[cnt + 1], m10_list[cnt + 1]
                if line_cross(m5, m5_next, m10, m10_next) == result_flag:
                    # 已经找到了第一个点
                    last_stage = 1
                    cnt = cnt + 1
                    point1_val = {"close": close_list[cnt], "cnt": cnt, "date": date}
                    continue

            # 寻找第2个点 5日线上穿20日线,已经存在 1 点
            if last_stage == 1:
                m5_next, m20_next = m5_list[cnt + 1], m20_list[cnt + 1]
                if line_cross(m5, m5_next, m20, m20_next) == result_flag:
                    # 已经找到了第二个点
                    last_stage = 2
                    cnt = cnt + 1
                    point2_val = {"close": close_list[cnt], "cnt": cnt, "date": date}
                    continue

            # 寻找第3个点 10日线上穿20日线,已经存在 2 点
            if last_stage == 2:
                m10_next, m20_next = m10_list[cnt + 1], m20_list[cnt + 1]
                if line_cross(m10, m10_next, m20, m20_next) == result_flag:
                    # 已经找到了第三个点
                    last_stage = 3
                    cnt = cnt + 1
                    point3_val = {"close": close_list[cnt], "cnt": cnt, "date": date}
                    # 打印节点
                    print_node(point1_val, point2_val, point3_val)
                    # 初始化寻找下一个价托点位
                    last_stage = 0
                    stage_cnt = 0
                    point1_val, point2_val, point3_val = {}, {}, {}
                    continue

            if last_stage > 0 and stage_cnt <= 7:
                stage_cnt = stage_cnt + 1
            else:
                # 初始化点位
                last_stage = 0
                stage_cnt = 0
                point1_val, point2_val, point3_val = {}, {}, {}

        cnt = cnt + 1


def print_node(point1, point2, point3):
    if point1 and point2 and point3:
        print("find condition !")
        print("point1 ", point1)
        print("point2 ", point2)
        print("point3 ", point3)


# 如果满足条件，上穿返回1，下穿返回-1，否则返回 0
def line_cross(m1, m1_next, m2, m2_next):
    if m1 < m2 and m1_next > m2_next:
        return 1
    if m1 > m2 and m1_next < m2_next:
        return -1
    return 0


if __name__ == '__main__':
    # 600690
    line_list = kline.query_k_line("600038", "20210101")
    close_list = []
    date_list = []
    cl_list = []
    for node in line_list:
        clos = float(node.split(",")[2])
        close_list.append(clos)
        date_list.append(node.split(",")[0])
        cl_list.append(clos)

    closes = pd.Series(close_list)
    ma5 = talib.SMA(closes, timeperiod=5)
    ma10 = talib.SMA(closes, timeperiod=10)
    ma20 = talib.SMA(closes, timeperiod=20)

    m5_list = ma5.tolist()
    ma10_list = ma10.tolist()
    ma20_list = ma20.tolist()

    find_support_model(date_list, m5_list, ma10_list, ma20_list, close_list, 1)

    # plt.figure(figsize=(1280, 320), dpi=24)

    plt.plot(date_list, cl_list, label="close")
    plt.plot(date_list, m5_list, label="m5")
    plt.plot(date_list, ma10_list, label="m10")
    plt.plot(date_list, ma20_list, label="m20")

    plt.title('均线图', fontsize=20)
    plt.xlabel("时间", fontsize=20)
    plt.ylabel("价格", fontsize=20)
    # 每隔30个单位展示一个坐标
    x_major_locator = MultipleLocator(30)
    ax = plt.gca()
    # ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)
    # 设置 x坐标轴的斜率 和 字体大小
    plt.xticks(rotation=-15, fontsize=15)
    plt.yticks(fontsize=15)

    # 添加网格，可有可无，只是让图像好看点
    plt.grid()
    # 展示图例，也就是 plot 中的 label 图标展示
    plt.legend()
    # 记得加这一句，不然不会显示图像
    plt.show()

    # plt.savefig('plot123_2.png', dpi=300)  # 指定分辨率保存
