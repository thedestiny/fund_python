# 从dfcf 抓取基金趋势数据进行分析

import requests
import json
import time
# 线性回归
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from sklearn import linear_model

# 类型枚举
# m 一个月 q 3个月 hy 6个月 y 一年
# try 3年 fiy 5年 sy 今年来 se 最大
#
# 重要指数对比
# 000300 沪深300 000905 中证500
# 000001 上证指数 399001 深证成指
# 399005 中小板  399006 创业板

# 数据访问地址
address = "http://api.fund.eastmoney.com/pinzhong/LJSYLZS?fundCode={}&indexcode={}&type={}"

headers = {
    'Host': 'api.fund.eastmoney.com',
    'Referer': 'http://fund.eastmoney.com/'
}


# 抓取趋势数据
def query_fund_trend_data(fund_code="011615", idx_code="000300", type="q"):
    req_url = address.format(fund_code, idx_code, type)

    response = requests.get(req_url, headers=headers, timeout=6000)
    resp_body = json.loads(response.text)
    print(resp_body)
    if "Data" in resp_body:
        return resp_body["Data"]
    return []


# 中文字体展示
font = FontProperties(fname=r"/System/Library/Fonts/PingFang.ttc", size=10)

def matrix(arr):
    result = []
    for node in arr:
        tmep = []
        tmep.append(node)
        result.append(tmep)
    return result

def run_plt(plt, size=None):
    plt.figure(figsize=size)
    plt.title('序列与涨幅数据', fontproperties=font)
    plt.xlabel('序列', fontproperties=font)
    plt.ylabel('涨幅', fontproperties=font)
    # x start x end + y start y end

    plt.grid(True)
    return plt

# 分析基金信息
def analyze_fund_info(fundCode):
    data = query_fund_trend_data(fundCode)
    if len(data) == 0:
        return
    # 基金列表数据 同类列表数据 指数数据列表
    fund_list, kind_list, idx_list = data[0]["data"], data[1]["data"], data[2]["data"]
    fund_rate = fund_list[-1][1]
    kind_rate = kind_list[-1][1]
    idx_rate = idx_list[-1][1]

    cnt, x_arr, y_arr, time_arr = 0, [], [], []
    for node in fund_list:
        timeArray = time.localtime(node[0] / 1000)
        # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        other_time = time.strftime("%Y-%m-%d", timeArray)
        x_arr.append(cnt)
        y_arr.append(node[1])
        time_arr.append(other_time)
        cnt += 1

    x_min, x_max, y_min, y_max = min(x_arr) - 2, max(x_arr) + 2, min(y_arr) - 2, max(y_arr) + 2

    # 设置最大值和最小值区间
    plt.axis([x_min, x_max, y_min, y_max])
    mat_x = matrix(x_arr)
    mat_y = matrix(y_arr)

    # 展示基金图像
    plt.plot(mat_x, mat_y, color="darkblue", linewidth=1, linestyle='--', marker='+', label="fund")

    model = linear_model.LinearRegression()

    model.fit(mat_x, mat_y)

    # 模拟值
    model_x = mat_x
    model_y = model.predict(model_x)

    plt.plot(model_x, model_y, 'g-', label="linear")

    b = model.intercept_[0]
    # 线性模型的系数
    k = model.coef_[0][0]
    score = model.score(mat_x, mat_y)
    print("k {} b {}".format(k, b))

    print('score: %.3f' % score)
    text = "k={:.6f}\nscore={:.6f}".format(k, score)
    # 添加文字
    plt.text(x_max * 0.6, y_max * 0.4, text)

    # 添加图例
    plt.legend()
    plt.show()

    return evaluate_score(fund_rate, idx_rate)


# 基金评分标准
def evaluate_score(rate, level):
    """
    基金评分标准
    基金和基准差值在[-1,1] 之间评分为 0,和基准表现相似，平庸
    基金和基准差值在(1,5)  之间评分为 1,基本跑赢标准，及格
    基金和基准差值在(5,10) 之间评分为 2,基本跑赢标准，优良
    基金和基准差值在(10,20)之间评分为 3,基本跑赢标准，
    基金和基准差值在(20 +) 评分为 4,基本跑赢标准，优秀

    :param rate: 基金表现
    :param level: 基准表现
    :return: 返回评分
    """

    diff = rate - level
    result = 0
    if diff >= -1 and diff <= 1:
        result = 0
    if abs(diff) > 1 and abs(diff) <= 5:
        result = 2
    if abs(diff) > 5 and abs(diff) <= 10:
        result = 3
    if abs(diff) > 10 and abs(diff) <= 20:
        result = 4
    if abs(diff) >= 20 and abs(diff) <= 40:
        result = 5
    if abs(diff) >= 40:
        result = 6
    if diff > 0:
        return result
    else:
        return 0 - result


if __name__ == '__main__':

    fund_code_list = ["011615"]

    for node in fund_code_list:
        analyze_fund_info(node)
