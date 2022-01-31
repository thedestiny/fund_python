import matplotlib.pyplot as plt
from matplotlib import rc
import fund_info.stock_k_line as kline
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import talib
from mplfinance.original_flavor import candlestick_ohlc


# 获取均线的数据，通过timeperiod参数来分别获取 5,10,20 日均线的数据。

def plot_chart(klines):

    data = {}
    close_list = []
    for node in klines:
        close_list.append(node.split(",")[2])

    closes = pd.Series(close_list)

    data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(closes, fastperiod=12, slowperiod=26,
                                                                      signalperiod=9)

    # 获取10日均线和30日均线
    data["ma5"] = talib.MA(closes, timeperiod=5)
    data["ma7"] = talib.MA(closes, timeperiod=7)
    data["ma10"] = talib.MA(closes, timeperiod=10)
    data["ma20"] = talib.MA(closes, timeperiod=20)
    data["ma30"] = talib.MA(closes, timeperiod=30)
    data["ma60"] = talib.MA(closes, timeperiod=60)
    data["ma120"] = talib.MA(closes, timeperiod=120)
    data["ma250"] = talib.MA(closes, timeperiod=250)

    # 获取rsi 相对强弱指数
    data["rsi"] = talib.RSI(closes, timeperiod=14)

    upper, middle, lower = talib.BBANDS(closes, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    data["upper"] = upper
    data["middle"] = middle
    data["lower"] = lower

    fig = plt.figure()  # 创建绘图区，包含四个子图
    fig.set_size_inches((20, 16))
    # 布林线 left, bottom, width, height
    ax_candle = fig.add_axes((0, 0.8, 1, 0.32))  # 蜡烛图子图
    ax_macd = fig.add_axes((0, 0.6, 1, 0.2), sharex=ax_candle)  # macd子图
    ax_rsi = fig.add_axes((0, 0.4, 1, 0.2), sharex=ax_candle)  # rsi子图
    ax_vol = fig.add_axes((0, 0.2, 1, 0.2), sharex=ax_candle)  # 成交量子图
    bol_line = fig.add_axes((0, 0.0, 1, 0.2), sharex=ax_candle)  # 布林线

    ohlc = []  # 存放行情数据，candlestick_ohlc 需要传入固定格式的数据
    row_number = 0
    date_list = []
    index_list = []
    for node in klines:
        arr = node.split(",")
        date, highp, lowp, openp, closep = arr[0], arr[3], arr[4], arr[1], arr[2]
        ohlc.append([row_number, openp, highp, lowp, closep])
        date_list.append(date)
        index_list.append(row_number)
        row_number = row_number + 1

    date_tickers = date_list  # 获取Date数据

    data["index"] = index_list

    def format_date(x, pos=None):
        # 由于前面股票数据在 date 这个位置传入的都是int
        # 因此 x=0,1,2,...
        # date_tickers 是所有日期的字符串形式列表
        if x < 0 or x > len(date_tickers) - 1:
            return ''
        return date_tickers[int(x)]


    # 绘制蜡烛图
    ax_candle.plot(data["index"], data["ma5"], label="MA5")
    ax_candle.plot(data["index"], data["ma10"], label="MA10")
    ax_candle.plot(data["index"], data["ma20"], label="MA20")
    ax_candle.plot(data["index"], data["ma60"], label="MA60")
    ax_candle.plot(data["index"], data["ma120"], label="MA120")
    ax_candle.plot(data["index"], data["ma250"], label="MA250")
    candlestick_ohlc(ax_candle, ohlc, colorup="r", colordown="g", width=0.8)

    ax_candle.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    ax_candle.xaxis.set_major_locator(ticker.MultipleLocator(6))  # 设置间隔为6个交易日
    ax_candle.grid(True)
    ax_candle.set_title("k线图展示", fontsize=20)
    ax_candle.legend()

    # 绘制MACD
    ax_macd.plot(data["index"], data["macd"], label="macd")
    ax_macd.bar(data["index"], data["macd_hist"] * 3, label="hist")
    ax_macd.plot(data["index"], data["macd_signal"], label="signal")
    ax_macd.set_title('MACD')
    ax_macd.legend()

    # 绘制RSI
    ax_rsi.set_ylabel("(%)")
    ax_rsi.plot(data["index"], [70] * len(data["index"]), label="overbought")
    ax_rsi.plot(data["index"], [30] * len(data["index"]), label="oversold")
    ax_rsi.plot(data["index"], data["rsi"], label="rsi", color='r')
    ax_rsi.set_title('RSI')
    ax2 = ax_rsi.twinx()
    ax2.plot(data["index"], data["Close"], label="价格", color='g')
    ax_rsi.legend()

    # 绘制成交量
    ax_vol.bar(data["index"], data["Volume"] / 1000000)
    ax_vol.set_ylabel("亿元")

    # 绘制bool
    bol_line.set_ylabel("%")
    bol_line.plot(data["index"], data["upper"], label="upper")
    bol_line.plot(data["index"], data["middle"], label="middle")
    bol_line.plot(data["index"], data["lower"], label="lower")

    bol_line.set_title('BOLL')
    bol_line.legend()

    # 保存图片到本地
    ## fig.savefig("./photos/" + title + ".png", bbox_inches="tight")

    # 这里个人选择不要plt.show()，因为保存图片到本地的
    plt.show()


if __name__ == '__main__':
    line_list = kline.query_k_line("600690")
    close_list = []
    for node in line_list:
        close_list.append(node.split(",")[2])
    closes = pd.Series(close_list)
    ma5 = talib.SMA(closes, timeperiod=5)
    ma10 = talib.SMA(closes, timeperiod=10)
    ma20 = talib.SMA(closes, timeperiod=20)
    print(ma5)
    plot_chart(line_list)
