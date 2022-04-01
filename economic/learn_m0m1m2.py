import requests
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator
import matplotlib as mpl

# 设置中文显示问题，防止乱码
mpl.rcParams['font.sans-serif'] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False

# https://data.eastmoney.com/cjsj/hbgyl.html

# https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=GJZB&sty=ZGZB&p=1&ps=200&mkt=11

req_url = "https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=GJZB&sty=ZGZB&p=1&ps=200&mkt=11"

if __name__ == "__main__":
    body = requests.get(req_url).text
    body = body.replace("(", "").replace(")", "")
    data_list = body.split("\",\"")

    # 定义数据
    date_list, m0_list, m1_list, m2_list = [], [], [], []

    for node in data_list:
        node = node.replace("]", "").replace("[", "").replace("\"", "")
        arr_list = node.split(",")
        date = arr_list[0]
        if date < "2011-01-01":
            continue
        # 时间数据
        date_list.append(date)
        # 数据操作存储
        m2_list.append(float(arr_list[2]))
        m1_list.append(float(arr_list[5]))
        m0_list.append(float(arr_list[8]))
        # 0 时间
        # 1-m2总量 2-m2同比增速 3-环比增速
        # 4-m1总量 5-m1同比增速 6-环比增速
        # 7-m0总量 8-m0同比增速 9-环比增速
        print(node)
    date_list.reverse()
    m0_list.reverse()
    m1_list.reverse()
    m2_list.reverse()
    x = np.asarray(date_list)
    m0_data = np.asarray(m0_list)
    m1_data = np.asarray(m1_list)
    m2_data = np.asarray(m2_list)

    plt.figure(figsize=(15, 5))  # 定义一个图像窗口
    plt.title('货币供应量')
    plt.xlabel('时间')
    plt.ylabel('百分比%')
    plt.plot(x, m0_data, label='m0', color="green")  # 绘制曲线 y1
    plt.plot(x, m1_data, label="m1", color="black")  # 绘制曲线 y2
    plt.plot(x, m2_data, label="m2", color="red")  # 绘制曲线 y2

    # 设置颜色填充，ppi 大于 cpi 时填充紫色，反之为深红色 并设置透明度
    # plt.fill_between(x, m1_data, m2_data, where=m1_data >= m2_data, facecolor='purple', alpha=0.3, interpolate=True)
    # plt.fill_between(x, m1_data, m2_data, where=m1_data < m2_data, facecolor='darkred', alpha=0.1, interpolate=True)

    # 把x轴的刻度间隔设置为12，既1年，并存在变量里
    x_major_locator = MultipleLocator(12)
    # 把y轴的刻度间隔设置为3，并存在变量里
    y_major_locator = MultipleLocator(3)
    # ax为两条坐标轴的实例
    ax = plt.gca()
    # 把x轴的主刻度设置为1的倍数
    ax.xaxis.set_major_locator(x_major_locator)
    # 把y轴的主刻度设置为10的倍数
    ax.yaxis.set_major_locator(y_major_locator)

    # 显示网格和图例 最后展示图形
    plt.legend()
    plt.grid()
    plt.show()

