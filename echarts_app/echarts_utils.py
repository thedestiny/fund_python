import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Kline, Line, Grid
from pyecharts.commons.utils import JsCode
from pyecharts import options as opts
from pyecharts.charts import Bar
import copy
import numpy as np
import talib
import stk_k_line as stk

# 设置数据保留位数
pd.set_option('display.float_format', '{:.2f}'.format)

def generate_ma(data, date_list, ma):
    """
    data df["收盘价"]
    date_list 时间序列
    ma 天数 5 10 20 30
    :param data:
    :return:
    """

    # 计算 10日线
    ma10 = data.rolling(window=ma).mean().dropna()
    start_date = ma10.index[0]
    # 10 日均线
    line_ma10 = Line()
    line_ma10.add_xaxis(date_list[start_date:])
    line_ma10.add_yaxis("ma" + str(ma), ma10.tolist(),
                        is_smooth=True,
                        is_symbol_show=False,  # 不显示均线的数据点符号
                        label_opts=opts.LabelOpts(is_show=False))  # 不显示均线的数据点标签
    line_ma10.set_global_opts(legend_opts=opts.LegendOpts(pos_left="right"))
    return line_ma10

def generate_kline(title, date_list, ohlc):
    """
     title 标题
     ohlc 日线数据
    :param title:
    :return:
    """

    # 创建 k线数据
    kline = Kline()
    kline.add_xaxis(date_list)
    kline.add_yaxis(title, ohlc,
                    markpoint_opts=opts.MarkPointOpts(
                        data=[
                            opts.MarkPointItem(type_="max", name="最高"),
                            opts.MarkPointItem(type_="min", name="最低"),
                            # opts.MarkPointItem(name="自定义", coord= [], value= 34)
                        ])
                    )

    # 设置语言为中文（可选，因为默认可能已经是中文）
    # 设置全局
    kline.set_global_opts(
        # legend_opts=opts.LegendOpts(pos_left="left"),
        legend_opts=opts.LegendOpts(is_show=True, pos_left="25%"),
        toolbox_opts=opts.ToolboxOpts(is_show=True, pos_top = "top"),
        xaxis_opts=opts.AxisOpts(is_scale=True),
        yaxis_opts=opts.AxisOpts(is_scale=True),
        datazoom_opts=[opts.DataZoomOpts(type_="slider", xaxis_index=[0, 1], range_start=50, range_end=100),
                       opts.DataZoomOpts(type_="inside", range_start=50, range_end=100)],
        title_opts=opts.TitleOpts(title="k线图")
    )

    return kline






def generate_ma_n(data, date_list, ma):
    """
    data df["收盘价"]
    date_list 时间序列
    ma 天数 5 10 20 30
    :param data:
    :return:
    """

    # 计算 10日线
    ma10 = data
    start_date = ma10.index[0]
    # 10 日均线
    line_ma10 = Line()
    line_ma10.add_xaxis(date_list[start_date:])
    line_ma10.add_yaxis("ma" + str(ma), ma10.tolist(),
                        is_smooth=True,
                        is_symbol_show=False,  # 不显示均线的数据点符号
                        label_opts=opts.LabelOpts(is_show=False))  # 不显示均线的数据点标签
    line_ma10.set_global_opts(legend_opts=opts.LegendOpts(pos_left="right"))
    return line_ma10












def generate_volume(date_list, vol_list):
    bar = Bar()
    bar.add_xaxis(date_list)
    bar.add_yaxis(series_name="成交量", y_axis=vol_list, xaxis_index=1, yaxis_index=1,
                  label_opts=opts.LabelOpts(is_show=False),
                  itemstyle_opts=opts.ItemStyleOpts(color=JsCode(
                      """
                      function(params) {
                            var colorList;
                            if (barData[params.dataIndex][1] > barData[params.dataIndex][0]) {
                                colorList = '#ef232a';
                            } else {
                                colorList = '#14b143';
                            }
                            return colorList;
                      }
                      """
                  ))
                  )
    bar.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_="category",
            grid_index=1,
            axislabel_opts=opts.LabelOpts(is_show=False),
        ),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    return bar


def generate_kline(title, date_list, ohlc):
    """
     title 标题
     ohlc 日线数据
    :param title:
    :return:
    """
    # 创建 k线数据
    kline = Kline()
    kline.add_xaxis(date_list)
    kline.add_yaxis(title, ohlc,
                    markpoint_opts=opts.MarkPointOpts(
                        data=[
                            opts.MarkPointItem(type_="max", name="最高"),
                            opts.MarkPointItem(type_="min", name="最低"),
                        ])
                    )
    # 设置语言为中文（可选，因为默认可能已经是中文）
    # 设置全局
    kline.set_global_opts(
        # legend_opts=opts.LegendOpts(pos_left="left"),
        legend_opts=opts.LegendOpts(is_show=True, pos_left="25%"),
        toolbox_opts=opts.ToolboxOpts(is_show=True, pos_top = "top"),
        xaxis_opts=opts.AxisOpts(is_scale=True),
        yaxis_opts=opts.AxisOpts(is_scale=True),
        datazoom_opts=[opts.DataZoomOpts(type_="slider", xaxis_index=[0, 1], range_start=50, range_end=100),
                       opts.DataZoomOpts(type_="inside", range_start=50, range_end=100)],
        title_opts=opts.TitleOpts(title="k线图")
    )

    return kline



# https://www.51cto.com/article/745892.html
# https://www.cnblogs.com/luoluoange/p/17787516.html
# https://blog.csdn.net/qq_36093530/article/details/145993425 文案修改
def query_future(code, name) -> Grid:
    print("code {} name {} ".format(code, name))

    # Date High Low Open Close Volume Amount Rate
    df = stk.query_stock_pandas("600519")
    df = df.reset_index(drop=True)

    # 计算均线数据
    sma5 = talib.SMA(df["Close"], 5)
    sma10 = talib.SMA(df["Close"], 10)
    sma20 = talib.SMA(df["Close"], 20)
    sma60 = talib.SMA(df["Close"], 60)
    # 日期数据和蜡烛线
    date_list = df["Date"].tolist()
    ohlc = df[["Open", "Close", "Low", "High"]].values.tolist()

    df["ma5"] = sma5
    df["ma10"] = sma10
    df["ma20"] = sma20
    df["ma60"] = sma60

    # 设置保留位数
    df['ma20'] = df['ma20'].round(2)
    df['ma60'] = df['ma60'].apply(lambda x: f"{x:.2f}")

    line_ma5 = generate_ma_n(df["ma5"], date_list, 5)
    line_ma10 = generate_ma_n(df["ma10"], date_list, 10)
    line_ma20 = generate_ma_n(df["ma20"], date_list, 20)
    line_ma60 = generate_ma_n(df["ma60"], date_list, 60)

    # 生成 k 线图
    kline = generate_kline(name, date_list, ohlc)

    # 加入 ohlc 日线图数据
    kline.overlap(line_ma5)
    kline.overlap(line_ma10)
    kline.overlap(line_ma20)
    kline.overlap(line_ma60)

    # 创建 grid
    grid = Grid()
    grid.add(kline, grid_opts=opts.GridOpts(pos_left="5%", pos_right="2%", height="70%"))

    # 添加多根线
    slope_line = Line()
    slope_line.add_xaxis(date_list)

    # bar_line = Bar()
    # bar_line.add_xaxis(date_list)

    # macd         dif 快线
    # macd_signal  dea 慢线
    # macd_hist    macd  能量柱
    df["macd"], df["macd_signal"], df["macd_hist"] = \
        talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

    # sma20_slope = np.round(talib.LINEARREG_SLOPE(sma20, timeperiod=10), 3)
    slope_line.add_yaxis(
        series_name="macd",
        y_axis=df["macd"],
        is_symbol_show=False,  # 不显示均线的数据点符号
        xaxis_index=1, yaxis_index=1,
        label_opts=opts.LabelOpts(is_show=False, position="insideLeft")
    ).set_global_opts(
        legend_opts=opts.LegendOpts(is_show=False, pos_left='60%',),
    )

    slope_line.add_yaxis(
        series_name="",
        y_axis=df["macd_signal"],
        xaxis_index=1, yaxis_index=1,
        is_symbol_show=False,  # 不显示均线的数据点符号
        label_opts=opts.LabelOpts(is_show=False, position="insideLeft")
    ).set_global_opts(
        legend_opts=opts.LegendOpts(is_show=False, pos_left='60%', ),
    )
    slope_line.add_yaxis(
        series_name="",
        y_axis=df["macd_hist"],
        xaxis_index=1, yaxis_index=1,
        # is_symbol_show=False,  # 不显示均线的数据点符号
        label_opts=opts.LabelOpts(is_show=False, position="insideLeft")
    ).set_global_opts(
        legend_opts=opts.LegendOpts(is_show=False, pos_left='60%', ),
    )
    # 斜率图 slope_line
    grid.add(
        slope_line,
        grid_opts=opts.GridOpts(
            pos_left="5%", pos_right="2%", pos_top="82%", height="13%"
        ), is_control_axis_index=False
    )
    # grid.add(
    #     bar_line,
    #     grid_opts=opts.GridOpts(
    #         pos_left="5%", pos_right="2%", pos_top="82%", height="13%"
    #     ), is_control_axis_index=False
    # )

    return grid


if __name__ == "__main__":

    # Date High Low Open Close Volume Amount Rate
    # 查询 pandas 数据
    pass


    # res = query_future("m2503", "豆粕2503", "1min")
    # res.render("test.html")