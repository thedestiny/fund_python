import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Kline, Line, Grid
from pyecharts.commons.utils import JsCode
from pyecharts import options as opts
from pyecharts.charts import Bar
import copy
import numpy as np



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
        # title_opts=opts.TitleOpts(title="k线图")
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

def query_future(code, name, period, ctx_n, rever) -> Grid:
    print("code {} name {} period {}".format(code, name, period))



    # k线上的均线
    line_ma10 = generate_ma_n(df["ma20"], date_list, 20)
    line_ma20 = generate_ma_n(df["ma60"], date_list, 60)
    line_ma120 = generate_ma120(df["ma120"], date_list, ma_list)



if __name__ == "__main__":
    res = query_future("m2503", "豆粕2503", "1min")
    res.render("test.html")