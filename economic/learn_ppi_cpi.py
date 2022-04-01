import requests
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator
import matplotlib as mpl

# https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=GJZB&sty=ZGZB&p=1&ps=200&mkt=22  ppi 数据
# https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=GJZB&sty=ZGZB&p=1&ps=200&mkt=19  cpi 数据

# cpi 和 ppi 请求数据地址
ppi_url = "https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=GJZB&sty=ZGZB&p=1&ps=200&mkt=22"
cpi_url = "https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=GJZB&sty=ZGZB&p=1&ps=200&mkt=19"
# ppi 和 cpi 请求地址相同，只是 mkt 不同，也就是传入的参数类型不同 ppi 为 22 cpi 为 21
req_url = "https://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=GJZB&sty=ZGZB&p=1&ps=200&mkt=19"

# 设置中文显示问题，防止乱码
mpl.rcParams['font.sans-serif'] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False

def query_time(nd):
    # cpi 和 ppi 的数据日期不一致，调整数据的展示日期区间
    return nd >= "2011-01-01" and nd <= "2025-12-01"

def query_data_list(url):
    """
    获取数据
    """
    # 去除 https 校验提醒信息 verify=False 忽略对证书的验证
    requests.packages.urllib3.disable_warnings()
    data = requests.get(url, verify=False).text
    # 通过浏览器控制台查看数据返回的结构，进行转换后存入一个 list
    data = data.replace("([\"", "").replace("\"])", "")
    arr_list = data.split("\",\"")
    # 临时打印结果
    print(arr_list)
    return arr_list





#
if __name__ == "__main__":
    # 查询 cpi 和 ppi 的数据
    list_cpi = query_data_list(cpi_url)
    list_ppi = query_data_list(ppi_url)

    # 需要将获取到的数据先倒序排列
    list_ppi.reverse()
    list_cpi.reverse()

    # 创建字典存放临时数据，key 为时间 value 为同步变化值
    ppi_dic, cpi_dic = {}, {}
    for lo in list_ppi:
        if lo:
            arr = lo.split(",")
            ppi_dic[arr[0]] = arr[1]

    for lo in list_cpi:
        if lo:
            arr = lo.split(",")
            cpi_dic[arr[0]] = arr[1]

    # 对 cpi 和ppi 数据的时间取交集然后进行顺序排序
    time_list_1 = list(set(cpi_dic.keys()) & set(ppi_dic.keys()))
    time_list_1.sort()

    # 过滤时间区间
    tmp_list = filter(query_time, time_list_1)
    # 创建变量存放处理结果
    ppi_list, cpi_list = [], []
    time_list = list(tmp_list)

    # 按照需要展示的时间从之前存放的字典中取出数据，四舍五入保留2为小数
    for nd in time_list:
        ppi_list.append(round(float(ppi_dic[nd]) - 100, 2))
        cpi_list.append(round(float(cpi_dic[nd]) - 100, 2))

    # 时间为 x 轴, ppi 和 cpi 均为 y 轴
    x = np.asarray(time_list)
    ppi = np.asarray(ppi_list)
    cpi = np.asarray(cpi_list)

    plt.figure(figsize=(15, 5))  # 定义一个图像窗口
    plt.title('cpi-ppi剪刀差图')
    plt.xlabel('时间')
    plt.ylabel('百分比%')
    plt.plot(x, ppi, label='ppi', color="green")  # 绘制曲线 y1
    plt.plot(x, cpi, label="cpi", color="black")  # 绘制曲线 y2
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
    # 把y轴的刻度范围设置为-10到20
    plt.ylim(-10, 20)
    # 设置颜色填充，ppi 大于 cpi 时填充紫色，反之为深红色 并设置透明度
    plt.fill_between(x, ppi, cpi, where=ppi >= cpi, facecolor='purple', alpha=0.3, interpolate=True)
    plt.fill_between(x, cpi, ppi, where=ppi < cpi, facecolor='darkred', alpha=0.1, interpolate=True)
    # 表示横线，参数(y的值，横线开始横坐标，横线结束横坐标)
    plt.hlines(0, "2011-01-01", "2021-10-01", color="red")
    # 表示竖线，参数(x的值，竖线开始纵坐标，竖线结束纵坐标)
    # 同理vlines和axvlines同样是垂直线，一个不会接触坐标轴，一个接触坐标轴。
    plt.vlines("2017-01-01", -10, 20, color="green")
    plt.axvline("2020-03-01", -10, 20, color="green")

    # 显示网格和图例 最后展示图形
    plt.legend()
    plt.grid()
    plt.show()
