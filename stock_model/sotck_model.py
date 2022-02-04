from matplotlib import rc
import fund_info.stock_k_line as kline
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import talib
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False
# 单位是inches
plt.rcParams['figure.figsize'] = (20.0, 8.0)

def plot_chart(data, title):
    fig = plt.figure()
    # 创建绘图区，包含四个子图
    fig.set_size_inches((40, 32))
    # 布林线 left, bottom, width, height
    ax_candle = fig.add_axes((0, 0.8, 1, 0.2))  # 蜡烛图子图即股票k线图
    ax_vol = fig.add_axes((0, 0.6, 1, 0.2), sharex=ax_candle)  # macd子图
    ax_macd = fig.add_axes((0, 0.4, 1, 0.2), sharex=ax_candle)  # rsi子图
    ax_rsi = fig.add_axes((0, 0.2, 1, 0.2), sharex=ax_candle)  # 成交量子图
    bol_line = fig.add_axes((0, 0.0, 1, 0.2), sharex=ax_candle)  # 布林线

    # 存放行情数据，candlestick_ohlc需要传入固定格式的数据
    ohlc = []
    row_number = 0
    for date, row in data.iterrows():
        date, highp, lowp, openp, closep = row[:5]
        ohlc.append([row_number, openp, highp, lowp, closep])
        row_number = row_number + 1

    # 将字符串格式日期转换为日期格式
    data['Date'] = pd.to_datetime(data['Date'])
    # 将日期列作为行索引
    # data.set_index(['Date'], inplace=True)
    date_tickers = data.Date.values  # 获取Date数据

    def format_date(x, pos=None):
        # 由于前面股票数据在 date 这个位置传入的都是int
        # 因此 x=0,1,2,...
        # date_tickers 是所有日期的字符串形式列表
        if x < 0 or x > len(date_tickers) - 1:
            return ''
        return date_tickers[int(x)]

    # 绘制蜡烛图
    ax_candle.plot(data.index, data["ma5"], label="MA5")
    ax_candle.plot(data.index, data["ma10"], label="MA10")
    ax_candle.plot(data.index, data["ma20"], label="MA20")
    ax_candle.plot(data.index, data["ma60"], label="MA60")
    ax_candle.plot(data.index, data["ma120"], label="MA120")
    ax_candle.plot(data.index, data["ma250"], label="MA250")

    candlestick_ohlc(ax_candle, ohlc, colorup="r", colordown="g", width=0.8)

    ax_candle.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    ax_candle.xaxis.set_major_locator(ticker.MultipleLocator(10))  # 设置间隔为6个交易日
    ax_candle.grid(True)
    ax_candle.set_title(title, fontsize=10)
    ax_candle.legend()

    # 绘制MACD
    ax_macd.plot(data.index, data["macd"], label="macd")
    ax_macd.bar(data.index, data["macd_hist"] * 3, label="hist")
    ax_macd.plot(data.index, data["macd_signal"], label="signal")
    ax_macd.set_title('MACD')
    ax_macd.legend()

    # 绘制RSI
    ax_rsi.set_ylabel("(%)")
    ax_rsi.plot(data.index, [70] * len(data.index), label="overbought")
    ax_rsi.plot(data.index, [30] * len(data.index), label="oversold")
    ax_rsi.plot(data.index, data["rsi"], label="rsi", color='r')
    ax_rsi.set_title('RSI')

    ax2 = ax_rsi.twinx()
    ax2.plot(data.index, data["Close"], label="价格", color='r')
    ax_rsi.legend()

    # 绘制成交量
    ax_vol.bar(data.index, data["Volume"] / 1000000)
    ax_vol.set_ylabel("亿元")

    # 绘制bool
    bol_line.set_ylabel("%")
    bol_line.plot(data.index, data["upper"], label="upper")
    bol_line.plot(data.index, data["middle"], label="middle")
    bol_line.plot(data.index, data["lower"], label="lower")

    bol_line.set_title('BOLL')
    bol_line.legend()

    # 保存图片到本地
    # fig.savefig("./photos/" + title + ".png", bbox_inches="tight")

    # 这里个人选择不要plt.show()，因为保存图片到本地的
    plt.show()


if __name__ == '__main__':
    line_list = kline.query_k_line("600690", "20210101")

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
