# 量化掘金

# coding=utf-8
from __future__ import print_function, absolute_import

import json
import datetime
from dateutil.relativedelta import relativedelta
import dateutil.relativedelta as dr
from gm.api import *

# 总体策略 买入要慢，卖出要快
# 1 macd 近一年的低位数据，死叉时买入

# pip3 install gm -i https://mirrors.aliyun.com/pypi/simple/

class trade_info:

    def __init__(self, code, max_price, min_price, total_num, total_cost, total_value, trade_list):
        """
        交易记录
        """
        self.code = code
        self.max_price = max_price
        self.min_price = min_price
        self.total_num = total_num
        # 买入总价格
        self.total_cost = total_cost
        self.total_value = total_value
        self.trade_list = trade_list
        self.max_date = None
        self.min_date = None
        self.stop_buy = False
        self.fixed_buy = 0
        self.clear = False

    def to_dict(self):
        return self.__dict__

class stock_trade:

    def __init__(self, code, name, idx, tim, price, buy_num, detail):
        """
        交易记录 代码 名称 买入指数点位 买入时间 买入价格 买入数量 买入描述
        """
        self.code = code
        self.name = name
        self.buy_idx = idx
        self.buy_tim = tim
        self.buy_price = price
        self.buy_num = buy_num
        self.buy_detail = detail
        # 卖出的情况
        self.sell_idx = None
        self.sell_tim = None
        self.sell_price = None
        self.sell_detail = None
        # 是否交易完成
        self.finish = False
    def to_dict(self):
        return self.__dict__

# 计算 kdj 数据
def calculate_kdj(data, n=9, m1=3, m2=3):
    low_min = data['low'].rolling(n).min()
    high_max = data['high'].rolling(n).max()
    data['RSV'] = (data['close'] - low_min) / (high_max - low_min) * 100
    data['K'] = data['RSV'].ewm(alpha=1/m1, adjust=False).mean()  # 近似SMA
    data['D'] = data['K'].ewm(alpha=1/m2, adjust=False).mean()
    data['J'] = 3 * data['K'] - 2 * data['D']

    data["K1"] = data.K.shift(1)
    data["D1"] = data.D.shift(1)
    return data
# 计算 rsi 数据
def calculate_rsi(data, window=14):
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))
    data["RSI1"] = data.RSI.shift(1)
    return data
# 计算 macd 数据
def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    data['EMA12'] = data['close'].ewm(span=fast_period, adjust=False).mean()
    data['EMA26'] = data['close'].ewm(span=slow_period, adjust=False).mean()
    data['DIF'] = data['EMA12'] - data['EMA26']
    data['DEA'] = data['DIF'].ewm(span=signal_period, adjust=False).mean()
    data['MACD'] = (data['DIF'] - data['DEA']) * 2
    data["MACD1"] = data.MACD.shift(1)
    data["DIF1"] = data.DIF.shift(1)
    data["DEA1"] = data.DEA.shift(1)
    # data["DIF1"] = data.DIF.shift(1)
    # data["DEA1"] = data.DEA.shift(1)
    return data
    # # 调用
    # data = get_kline_data()  # 假设这是获取K线数据的函数
    # data_with_macd = calculate_macd(data)
# 计算 boll 数据
def calculate_boll(data, window = 20, num_std =2):
   """
   data 收盘价数据
   windows 移动平均窗口周期
   num_std 标准差倍数
   """
   # 计算中轨（20日简单移动平均）
   data['middle'] = data['close'].rolling(window=window).mean()

   # 计算标准差（注意：设置 ddof=0 使用总体标准差）
   data['std'] = data['close'].rolling(window=window).std(ddof=0)
   # 计算上下轨
   data['upper'] = data['middle'] + num_std * data['std']
   data['lower'] = data['middle'] - num_std * data['std']

   data["middle1"] = data.middle.shift(1)
   data["upper1"] = data.upper.shift(1)
   data["lower1"] = data.lower.shift(1)
   return data


# 计算交易价格,四舍五入
def cal_code_trade_price(price, rate):
    return round(price * (1 + rate), 3)

def cal_buy_num(tot_num, rate):
    if tot_num * rate <= 300:
        return 300
    else:
        res = int(tot_num * rate) // 100
        return res * 200

def query_code_trade_info(context, code, price, current_date):
    tad_list = context.trade_list
    res_list = []
    for ele in tad_list:
        if code == ele.code and not ele.finish:
            res_list.append(ele)
    if len(res_list) == 0:
        return None
    # 获取交易的最大价格, 最小价格，总数
    max_price = max(res_list, key=lambda ele: ele.buy_price).buy_price
    min_price = min(res_list, key=lambda ele: ele.buy_price).buy_price
    # 最大的日期
    max_date = max(res_list, key=lambda ele: ele.buy_tim).buy_tim
    min_date = min(res_list, key=lambda ele: ele.buy_tim).buy_tim
    # total_num = sum(ele.buy_num for ele in res_list)
    total_num = sum(map(lambda obj: obj.buy_num, res_list))
    # 买入总价格
    total_cost = sum(map(lambda obj: obj.buy_price * obj.buy_num, res_list))
    total_value = sum(map(lambda obj: price * obj.buy_num, res_list))
    trade_inf = trade_info(code, max_price, min_price, total_num, total_cost, total_value, res_list)
    trade_inf.max_date = max_date
    trade_inf.min_date = min_date
    # 计算上次买入的时间差
    differ = relativedelta(current_date, max_date)

    # 价差超过 10%, 停止常规买入, 买入数量超过 1000，且亏损
    # 1最大值与最小值的价差超过10%
    # 2当前价格大于平均价格
    # 3持有量大于1000且亏损
    if ((max_price - min_price) / max_price > 0.1 or price > (max_price + min_price)/2) or (total_num >= 1000 or total_value < total_cost):
        trade_inf.stop_buy = True
    else:
        trade_inf.stop_buy = False

    # 亏损状态拉长时间定投,每次投入 10%
    # 价差大于10% and 且当前价格小于最小价格 1.1 而且 间隔大于 10
    if (max_price - min_price) / max_price > 0.1 and price < min_price * 1.05 and differ.days > 5:
        trade_inf.fixed_buy = cal_buy_num(total_num, .2)
    else:
        trade_inf.fixed_buy = 0
    # 如果盈利 30% ，清仓
    if total_value > total_cost*1.4 > 0:
        trade_inf.clear = True
    else:
        trade_inf.clear = False

    return trade_inf



def query_code_pd(context, code_list):
    # 开始和结束时间
    st_time = context.backtest_start_time
    ed_time = context.backtest_end_time[:10]

    # 计算开始时间
    dat = datetime.datetime.strptime(st_time, '%Y-%m-%d %H:%M:%S')
    # date_str = current_date.strftime("%Y-%m-%d")
    dat = dat + dr.relativedelta(years=-1)
    st_date_str = dat.strftime("%Y-%m-%d")

    """
    查询数据的pandas 数据
    """
    data_dict = {}
    for ele in code_list:
        data = history(symbol=ele, frequency='1d', start_time=st_date_str, end_time=ed_time,
                       adjust=ADJUST_PREV, df=True)
        data = data[["symbol", "open", "high", "low", "close", "volume", "amount", "pre_close", "bob"]]
        # data = data.apply()
        data['bob'] = data['bob'].apply(lambda x: x.strftime('%Y-%m-%d'))
        # 计算指标 macd kdj rsi boll
        data = calculate_macd(data)
        data = calculate_kdj(data)
        data = calculate_rsi(data)
        data = calculate_boll(data)
        data_dict[ele] = data
    return data_dict

# 策略中必须有init方法
def init(context):
    # 订阅苏泊尔股票（002032.SZ）的日线数据
    # SHSE 上交所  SZSE 深交所 'SZSE.002032',
    # SHSE.601318  SZSE.000063  SZSE.002475 'SZSE.002475', 'SZSE.002032',
    # context.symbols = ['SZSE.002032', 'SHSE.600690'] 'SZSE.002032', 'SZSE.002032',
    code_list = ['SZSE.002583']
    # 订阅行情数据
    subscribe(symbols=code_list, frequency='1d', count=2000)
    # 查询股票基本信息
    code_pds = get_symbol_infos(sec_type1=1010, symbols=code_list, df=True)
    # 计算指标 macd kdj rsi

    data_dict = query_code_pd(context, code_list)
    context.data_dict = data_dict

    # print(code_pds)
    symbol_dict = {}
    # 循环 pandas 对象
    for t in range(len(code_pds)):
        start_idx = code_pds.index[t]  # 设置 index
        code = code_pds['symbol'].loc[start_idx]
        name = code_pds['sec_name'].loc[start_idx]
        symbol_dict[code] = name
    # 设置上下文
    context.symbol_dict = symbol_dict
    # 初始化参数
    context.buy_threshold = -0.04  # 买入阈值-4%
    context.sell_threshold = 0.5  # 卖出阈值+6%
    context.positions = []  # 记录持仓信息（价格，日期）
    context.last_buy_price = None  # 最近买入价
    # 交易记录和均线数据
    context.trade_list = []
    context.ma_num = 20

def on_bar(context, bars):
    # order_value 指定价值委托
    # order_volume 指定量委托
    # print(bars)
    # bars 标的k线行情数据
    bar = bars[0]
    # 代码 收盘价 最低价 最高价 当前日期
    code = bar.symbol
    current_price = bar.close
    current_low = bar.low
    current_high = bar.high
    current_date = bar.bob.date()
    # 当前时间的字符串
    date_str = current_date.strftime("%Y-%m-%d")
    tmp = current_date + dr.relativedelta(years=-1)
    before_date_str = tmp.strftime("%Y-%m-%d")
    # 获取过去20个交易日的数据
    data = context.data(symbol=code, frequency='1d', count=context.ma_num, fields='close,low,high,eob,bob')
    # print(data)
    # 计算均线，并获取最近20日的平均价
    data['ma20'] = data['close'].rolling(window=context.ma_num).mean()
    # 最近 20日平均价格
    ma20 = data['ma20'].loc[context.ma_num - 1]
    print("code {}  ma20 {} current_date {} current_price {} ".format(code, ma20, current_date, current_price))
    # 获取上一个交易日的收盘价
    yes_close = data["close"].loc[context.ma_num - 2]
    # 计算当日的最大跌幅
    ma_low_rate = current_low / yes_close - 1
    # 计算当日跌幅和最近20日平均价
    low_rate = current_low / ma20 - 1
    # 买入标记
    buy_flag = True
    trade_info = query_code_trade_info(context, code, current_price, current_date)
    if trade_info is not None:
        print("trade_info ", trade_info.to_dict())
        buy_flag = not trade_info.stop_buy
    # 在最后的交易日期打印交易明细 context.backtest_start_time[:10]
    # if date_str == "2025-02-17" and context.trade_list:
    # 最后的交易日
    if date_str == context.backtest_end_time[:10] and context.trade_list:
        td_list = context.trade_list
        td_list = sorted(td_list, key=lambda entity: entity.buy_tim, reverse=False)
        for element in td_list:
            print("final trade ", element.to_dict())
    # 获取可用资金
    cash = context.account().cash['available']
    # macd 买入条件
    low_macd_trade_condition(bar,  context)
    # boll 交易条件
    low_boll_trade_condition(bar, context)

    # 当天的跌幅买入标准
    if low_rate < 0 and buy_flag:
        # 跌幅大于 6% 买入
        if low_rate < -0.062:
            buy_price = cal_code_trade_price(yes_close, -0.062)
            order_volume(symbol=code, volume=100, side=OrderSide_Buy, order_type=OrderType_Limit,
                         position_effect=PositionEffect_Open, price=buy_price)
            ele = stock_trade(code=code, name=context.symbol_dict.get(code), idx=0, tim=current_date, price=buy_price,
                              buy_num=100, detail="跌幅大于6%买入")
            context.trade_list.append(ele)
        # 跌幅大于 4%,触发买入条件
        if low_rate < -0.042:
            buy_price = cal_code_trade_price(yes_close, -0.041)
            order_volume(symbol=code, volume=200, side=OrderSide_Buy, order_type=OrderType_Limit,
                         position_effect=PositionEffect_Open, price=buy_price)
            ele = stock_trade(code=code, name=context.symbol_dict.get(code), idx=0, tim=current_date, price=buy_price,
                              buy_num=200, detail="跌幅大于4%买入")
            context.trade_list.append(ele)

    # 最近20天的平均价格判断条件
    if ma_low_rate < -0.15 and buy_flag:
        buy_price = cal_code_trade_price(ma20, -0.15)
        order_volume(symbol=code, volume=300, side=OrderSide_Buy, order_type=OrderType_Limit,
                     position_effect=PositionEffect_Open, price=buy_price)
        ele = stock_trade(code=code, name=context.symbol_dict.get(code), idx=0, tim=current_date, price=buy_price,
                          buy_num=300, detail="ma20跌幅大于10%买入")
        context.trade_list.append(ele)

    # 定投模式,收盘价买入
    if trade_info is not None and trade_info.fixed_buy > 0:
        order_volume(symbol=code, volume=trade_info.fixed_buy, side=OrderSide_Buy, order_type=OrderType_Limit,
                     position_effect=PositionEffect_Open, price=current_price)
        ele = stock_trade(code=code, name=context.symbol_dict.get(code), idx=0, tim=current_date, price=current_price,
                          buy_num=trade_info.fixed_buy, detail="定投模式买入")
        context.trade_list.append(ele)

    # 买入后,按照买入价格，每跌8%阶梯加仓
    if len(context.trade_list) > 0:
        tmp_list = sorted(context.trade_list, key=lambda entity: entity.buy_tim, reverse=False)
        last_ele = tmp_list[-1]
        # 最后一次买入价格跌 8% 买入
        if last_ele.buy_price * 0.92 > current_low:
            b_price = round(last_ele.buy_price * 0.92, 3)
            order_volume(symbol=code, volume=200, side=OrderSide_Buy, order_type=OrderType_Limit,
                         position_effect=PositionEffect_Open, price=b_price)
            ele = stock_trade(code=code, name=context.symbol_dict.get(code), idx=0, tim=current_date,
                              price=b_price,
                              buy_num=200, detail="最后一次价格0.92定投模式买入")
            context.trade_list.append(ele)

    if trade_info is not None and trade_info.clear:
        td_list = trade_info.trade_list
        for element in td_list:
            tag_price = current_price
            # 调仓到目标持仓量
            print("sell date {} code {} price {} num {}".format(current_date, code, tag_price, element.buy_num))
            order_target_volume(symbol=code, volume= element.buy_num, position_side=PositionSide_Long,
                                    order_type=OrderType_Limit, price=tag_price)
            element.sell_tim = current_date
            element.sell_price = tag_price
            element.finish = True
            element.sell_detail = "清仓卖出"

    if trade_info is not None:
        # 交易列表和股票总数
        td_list = trade_info.trade_list
        tot_num = trade_info.total_num
        for element in td_list:
            tag_price = element.buy_price * (1 + context.sell_threshold)
            if current_date > element.buy_tim and current_high >= tag_price:
                # 调仓到目标持仓量
               print("sell date {} code {} price {} num {}".format(current_date, code, tag_price, element.buy_num))
               order_target_volume(symbol=code, volume=tot_num - element.buy_num, position_side=PositionSide_Long,
                                order_type=OrderType_Limit, price=tag_price)
               element.sell_tim = current_date
               element.sell_price = tag_price
               element.finish = True
               element.sell_detail = "涨幅卖出"

    # (1) 卖出逻辑：遍历持仓检查止盈
    for position in list(context.positions):
        buy_price, buy_date = position
        # T+1限制且达到止盈
        if current_date > buy_date and current_price >= buy_price * (1 + context.sell_threshold):
            pass
            # 计算持仓数量（简化处理，实际需查询持仓）调整仓位到指定百分比
            # order_target_percent(symbol=code, percent=0.2, order_type=OrderType_Market,
            #                      position_side=PositionSide_Long)
            # 调仓到目标持仓量
            # order_target_volume(symbol=code, volume=10000, position_side=PositionSide_Long,
            #                     order_type=OrderType_Limit, price=13)

            # context.positions.remove(position)
            # print('卖出触发 价格:', current_price, '买入价:', buy_price)

    # (2) 买入逻辑
    # 获取最近20日收盘价,获取pandas 数据
    # history = history_n(symbol=code, frequency='1d', count=20, fields='close,low,high,bob,eob', df=True)

# boll 交易条件
def low_boll_trade_condition(bar, context):
    code = bar.symbol
    current_date = bar.bob.date()
    # 当前时间的字符串
    date_str = current_date.strftime("%Y-%m-%d")
    tmp = current_date + dr.relativedelta(years=-1)
    before_date_str = tmp.strftime("%Y-%m-%d")

    # 当前时间的字符串
    date_str = current_date.strftime("%Y-%m-%d")
    # macd 买入条件 代码技术指标数据
    code_pd = context.data_dict[code]
    current_low = bar.low
    # 查询当前日期之前的数据
    # 使用between()方法
    # filtered_df = df[(df['age'].between(30, 40))]
    filter_pd = code_pd[(code_pd["bob"] <= date_str) & (code_pd["bob"] >= before_date_str)]
    # filter_pd = filter_pd.dropna(axis=0, inplace=True)
    # dea 最近一年的数据
    min_dea = filter_pd["DEA"].min()
    # 当天的 pandas 数据
    cur_pd = filter_pd.iloc[-1]
    low, low1 = cur_pd['lower'], cur_pd['lower1']
    # boll 线开口向下且最低值比下轨低 5%
    if low < low1 and current_low * 1.06 < low:
        buy_price = round(low * 0.945, 3)
        order_volume(symbol=code, volume=500, side=OrderSide_Buy, order_type=OrderType_Limit,
                     position_effect=PositionEffect_Open, price=buy_price)
        ele = stock_trade(code=code, name=context.symbol_dict.get(code), idx=0, tim=current_date, price=buy_price,
                          buy_num=500, detail="boll条件买入")
        context.trade_list.append(ele)

# macd 交易条件
def low_macd_trade_condition(bar, context):

    # , current_date, current_high, current_low, date_str  before_date_str, code,

    code = bar.symbol
    current_price = bar.close
    current_low = bar.low
    current_high = bar.high
    current_date = bar.bob.date()
    # 当前时间的字符串
    date_str = current_date.strftime("%Y-%m-%d")
    tmp = current_date + dr.relativedelta(years=-1)
    before_date_str = tmp.strftime("%Y-%m-%d")

    # macd 买入条件 代码技术指标数据
    code_pd = context.data_dict[code]
    # 查询当前日期之前的数据
    # 使用between()方法
    # filtered_df = df[(df['age'].between(30, 40))]
    filter_pd = code_pd[(code_pd["bob"] <= date_str) & (code_pd["bob"] >= before_date_str)]
    # filter_pd = filter_pd.dropna(axis=0, inplace=True)
    # dea 最近一年的数据
    min_dea = filter_pd["DEA"].min()
    # 当天的 pandas 数据
    cur_pd = filter_pd.iloc[-1]
    # for t in range(len(cur_pd)):
    # start_idx = cur_pd.index[t]  # 设置 index
    # sym = cur_pd['symbol']
    # print(sym)
    # code = cur_pd['symbol']
    dea = cur_pd['DEA']
    dea1 = cur_pd['DEA1']
    dif = cur_pd['DIF']
    dif1 = cur_pd['DIF1']
    # 低位金叉 触发买入条件
    if min_dea * 0.95 <= dea and (dif1 < dea1 and dif > dea) and dea < 0:
        buy_price = round((current_high + current_low) / 2, 2)
        order_volume(symbol=code, volume=500, side=OrderSide_Buy, order_type=OrderType_Limit,
                     position_effect=PositionEffect_Open, price=buy_price)
        ele = stock_trade(code=code, name=context.symbol_dict.get(code), idx=0, tim=current_date, price=buy_price,
                          buy_num=500, detail="macd条件买入")
        context.trade_list.append(ele)

    return code

def on_order_status(context, order):
    # 算法子单已成
    if order['status'] == 3:
        print("order is ", order)







if __name__ == '__main__':
    '''
        strategy_id策略ID, 由系统生成
        filename文件名, 请与本文件名保持一致,默认为 main.py
        mode运行模式, 实时模式:MODE_LIVE回测模式:MODE_BACKTEST
        token绑定计算机的ID, 可在系统设置-密钥管理中生成
        backtest_start_time回测开始时间
        backtest_end_time回测结束时间
        backtest_adjust股票复权方式, 不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
        backtest_initial_cash回测初始资金
        backtest_commission_ratio回测佣金比例
        backtest_slippage_ratio回测滑点比例
        backtest_match_mode市价撮合模式，以下一tick/bar开盘价撮合:0，以当前tick/bar收盘价撮合：1
        '''
    run(strategy_id='0f8e847b-ec75-11ef-a9f9-00ff324de186',
        filename='zhangdie_01.py',
        mode=MODE_BACKTEST,
        token='48edc73999985411f77b7feebb7e5397c43c14ce',
        backtest_start_time='2022-01-01 08:00:00',
        backtest_end_time='2025-02-24 16:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=1000000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001,
        backtest_match_mode=1)
