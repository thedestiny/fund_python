from matplotlib import rc
import fund_info.stock_k_line as kline
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import talib
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib as mpl
import mplfinance as mpf
# 用于定制线条颜色
from cycler import cycler

mpl.rcParams['font.sans-serif'] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False
# 单位是inches
plt.rcParams['figure.figsize'] = (20.0, 8.0)

def plot_chart(data, title):
    # 将字符串格式日期转换为日期格式
    data['Date'] = pd.to_datetime(data['Date'])
    # 将日期列作为行索引
    data.set_index(['Date'], inplace=True)
    symbol = title
    # 设置基本参数
    # type 绘制图形的类型 有candle, renko, ohlc, line等
    # 此处选择candle,即K线图
    # mav(moving average):均线类型,此处设置7,30,60日线
    # volume:布尔类型，设置是否显示成交量，默认False
    # title:设置标题
    # y_label:设置纵轴主标题
    # y_label_lower:设置成交量图一栏的标题
    # figratio:设置图形纵横比
    # figscale:设置图形尺寸(数值越大图像质量越高)
    kwargs = dict(
        type='candle',
        mav=(7, 30, 60),
        volume=True,
        title='\nstock %s k线图' % (symbol),
        ylabel='价格',
        ylabel_lower='交易量',
        figratio=(15, 10),
        figscale=5)

    # 设置marketcolors
    # up:设置K线线柱颜色，up意为收盘价大于等于开盘价
    # down:与up相反，这样设置与国内K线颜色标准相符
    # edge:K线线柱边缘颜色(i代表继承自up和down的颜色)，下同。详见官方文档)
    # wick:灯芯(上下影线)颜色
    # volume:成交量直方图的颜色
    # inherit:是否继承，选填
    mc = mpf.make_marketcolors(
        up='red',
        down='green',
        edge='i',
        wick='i',
        volume='in',
        inherit=True)

    # 设置图形风格
    # gridaxis:设置网格线位置
    # gridstyle:设置网格线线型
    # y_on_right:设置y轴位置是否在右
    s = mpf.make_mpf_style(
        gridaxis='both',
        gridstyle='-.',
        y_on_right=False,
        marketcolors=mc)

    # 设置均线颜色，配色表可见下图
    # 建议设置较深的颜色且与红色、绿色形成对比
    # 此处设置七条均线的颜色，也可应用默认设置
    mpl.rcParams['axes.prop_cycle'] = cycler(
        color=['dodgerblue', 'deeppink',
               'navy', 'teal', 'maroon', 'darkorange',
               'indigo'])

    # 设置线宽
    mpl.rcParams['lines.linewidth'] = 1.5

    # 图形绘制
    # show_nontrading:是否显示非交易日，默认False
    # savefig:导出图片，填写文件名及后缀
    # mpf.plot(data,
    #          **kwargs,
    #          style=s,
    #          show_nontrading=False,
    #          savefig='A_stock-%s %s_candle_line'
    #                  % (symbol, period) + '.jpg')

    mpf.plot(data,
             **kwargs,
             style=s,
             show_nontrading=False,
             )

    plt.xticks(rotation=-15, fontsize=15)
    plt.yticks(fontsize=15)

    plt.show()


if __name__ == '__main__':
    line_list = kline.query_k_line("600690", "20211001")

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
