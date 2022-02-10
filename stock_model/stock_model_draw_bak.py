import stock_info.stock_k_line as kline
import matplotlib.pyplot as plt
import pandas as pd
import talib
import matplotlib as mpl
import mplfinance as mpf
# 用于定制线条颜色
from cycler import cycler

mpl.rcParams['font.sans-serif'] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False
# 单位是inches
plt.rcParams['figure.figsize'] = (20.0, 8.0)

# 绘制图形
def plot_chart(data, title):
    # 将字符串格式日期转换为日期格式
    data['Date'] = pd.to_datetime(data['Date'])
    # 将日期列作为行索引
    data.set_index(['Date'], inplace=True)
    # 设置基本参数
    kwargs = dict(
        type='candle', mav=(5, 10, 20), volume=True, xrotation=15, title='stock_info %s k线图' % (title),
        ylabel='价格', ylabel_lower='交易量', figratio=(15, 10), figscale=1.5)

    # 设置图形的颜色 上涨和下跌的颜色设置
    mc = mpf.make_marketcolors(up='red', down='green', edge='i', wick='i', volume='in', inherit=True)

    # 设置图形风格 中文展示乱码设置 表格 grid 展示
    s = mpf.make_mpf_style(rc={'font.family': 'SimHei', 'axes.unicode_minus': 'False'},
                           gridaxis='both', gridstyle='-.', y_on_right=False, marketcolors=mc)

    # 设置均线颜色，配色表可见下图
    mpl.rcParams['axes.prop_cycle'] = cycler(
        color=['dodgerblue', 'deeppink', 'navy', 'teal', 'maroon', 'darkorange', 'indigo'])
    # 设置图形展示的线宽
    mpl.rcParams['lines.linewidth'] = .5
    # 传入数据展示 基本设置参数 横坐标日期格式化 图形展示 非交易日不展示
    mpf.plot(data, **kwargs, datetime_format='%Y-%m-%d', style=s, show_nontrading=False)
    # 图形绘制展示
    plt.show()


if __name__ == '__main__':
    line_list = kline.query_k_line("300059", "20211001")

    date_list, open_list, close_list, high_list, low_list = [], [], [], [], []
    # 成交量 成交额
    vol_list, amt_list = [], []

    for node in line_list:
        arr = node.split(",")
        date_list.append(arr[0])
        open_list.append(float(arr[1]))
        close_list.append(float(arr[2]))
        high_list.append(float(arr[3]))
        low_list.append(float(arr[4]))
        vol_list.append(float(arr[5]))
        amt_list.append(float(arr[6]))

    # 组装 dataframe 数据
    data = pd.DataFrame({
        "Date": date_list,
        "High": high_list,
        "Low": low_list,
        "Open": open_list,
        "Close": close_list,
        "Volume": vol_list,
        "Amount": amt_list
    })

    # date_series = data['Date']
    # print(date_series)

    # 计算 macd 数据
    # talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data['Close'], fastperiod=12, slowperiod=26,
                                                                      signalperiod=9)

    # 计算均线数据
    data["ma5"] = talib.MA(data["Close"], timeperiod=5)
    data["ma7"] = talib.MA(data["Close"], timeperiod=7)
    data["ma10"] = talib.MA(data["Close"], timeperiod=10)
    data["ma20"] = talib.MA(data["Close"], timeperiod=20)
    data["ma30"] = talib.MA(data["Close"], timeperiod=30)
    data["ma60"] = talib.MA(data["Close"], timeperiod=60)
    data["ma120"] = talib.MA(data["Close"], timeperiod=120)
    data["ma250"] = talib.MA(data["Close"], timeperiod=250)

    # 计算 rsi 相对强弱指数
    data["rsi"] = talib.RSI(data["Close"], timeperiod=14)

    # 计算 boll 线数据
    upper, middle, lower = talib.BBANDS(data["Close"], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    data["upper"] = upper
    data["middle"] = middle
    data["lower"] = lower

    # KDJ 值对应的函数是 STOCH
    data['slowk'], data['slowd'] = talib.STOCH(
        data['High'].values,
        data['Low'].values,
        data['Close'].values,
        fastk_period=9,
        slowk_period=3,
        slowk_matype=0,
        slowd_period=3,
        slowd_matype=0)
    # 求出J值，J = (3*K)-(2*D)
    data['slowj'] = list(map(lambda x, y: 3 * x - 2 * y, data['slowk'], data['slowd']))

    plot_chart(data, "数据展示")

    print(data)
