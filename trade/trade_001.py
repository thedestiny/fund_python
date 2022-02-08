import backtrader as bt
# from backtrader.feeds import PandasData
import datetime as datetime
import pandas as pd
import fund_info.stock_k_line as kline


# 创建策略继承bt.Strategy
class Strategy001(bt.Strategy):

    params = dict(period=20, hold=5)
    # 打印日志记录
    def log(self, txt, dt=None, doprint=False):
        """
        日志函数，用于统一输出日志格式
        """
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))
    # 通知订单交易情况
    def notify_order(self, order):
        """
        通知订单状态
        """
        if order.status in [order.Submitted, order.Accepted]:
            # 如订单已被处理，则不用做任何事情
            return

        # 检查订单是否完成
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '已买入, 价格: %.2f, 费用: %.2f, 佣金 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

            elif order.issell():
                self.log('已卖出, 价格: %.2f, 费用: %.2f, 佣金 %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            # 记录当前交易数量
            self.bar_executed = len(self)

        # 订单因为缺少资金之类的原因被拒绝执行
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            # 订单取消/保证金不足/拒绝
            self.log('Order Canceled/Margin/Rejected')

        # 订单状态处理完成，设为空
        self.order = None
    # 交易状态通知
    def notify_trade(self, trade):
        """
        交易成果
        """
        if not trade.isclosed:
            return

        # 显示交易的毛利率和净利润
        self.log('trade profit, cross %.2f, net %.2f' %
                 (trade.pnl, trade.pnlcomm), doprint=True)
        self.log('交易利润, 毛利润 %.2f, 净利润 %.2f' %
                 (trade.pnl, trade.pnlcomm))
    # 初始化数据
    def __init__(self):

        # 初始化相关数据
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # 五日移动平均线
        self.sma5 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=5)
        # 十日移动平均线
        self.sma10 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=10)

        # 加入均线指标 self.params.maperiod
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=20)

        # 绘制图形时候用到的指标
        # 指数均线
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # 加权均线
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25, subplot=True)
        # 慢随机指数
        bt.indicators.StochasticSlow(self.datas[0])
        # 异同移动平均线
        bt.indicators.MACDHisto(self.datas[0])
        # 相对强弱指数
        rsi = bt.indicators.RSI(self.datas[0])
        # 相对强弱指数
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # 平均真实波动范围
        bt.indicators.ATR(self.datas[0], plot=False)
    # 核心的交易策略
    def next(self):
        # 记录收盘价
        self.log('Close, %.2f' % self.dataclose[0])
        # 是否正在下单，如果是的话不能提交第二次订单
        if self.order:
            return
        # 是否已经买入
        if not self.position:
            # 还没买，如果 MA5 > MA10 说明涨势，买入
            if self.sma5[0] > self.sma10[0]:
                self.log('buy create, %.2f' % (self.dataclose[0]), doprint=True)
                self.order = self.buy()

        else:
            # 已经买了，如果 MA5 < MA10 ，说明跌势，卖出
            if self.sma5[0] < self.sma10[0]:
                self.log('sell create, %.2f' % (self.dataclose[0]), doprint=True)
                self.order = self.sell()
    # 模型回测介绍时打印
    def stop(self):
        self.log(u'(金叉死叉有用吗) Ending Value %.2f' %
                 (self.broker.getvalue()), doprint=True)


# 查询股票数据的变动信息
def query_stock_rate(code, start_date="20210101"):
    line_list = kline.query_k_line(code, start_date)

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
        "Date": date_list, "High": high_list, "Low": low_list,
        "Open": open_list, "Close": close_list, "Volume": vol_list, "Amount": amt_list
    })
    # 将字符串设置为日期格式
    data["Date"] = pd.to_datetime(data["Date"])
    # 修改列名并进行替换
    data.rename(
        columns={"Date": "date", "High": "high", "Low": "low", "Close": "close", "Open": "open", "Volume": "volume",
                 "Amount": "amount"}, inplace=True)
    # 添加列
    data["openinterest"] = 0.0
    # 设置日期为索引
    data.set_index(keys=['date'], inplace=True)
    # 删除字段
    data.drop(["amount"], inplace=True, axis=1)
    # 打印数据的前4列，并打印pandas的信息
    print(data.head(4))
    print(data.info())
    # 格式化后的数据
    format_data = bt.feeds.PandasDirectData(dataname=data, open=3, high=1, low=2, close=4, volume=5, openinterest=-1,
                                            fromdate=datetime.datetime(2021, 1, 1), todate=datetime.datetime(2030, 2, 2)
                                            )
    return format_data


if __name__ == '__main__':
    # 创建引擎对象
    cerebro = bt.Cerebro()
    # 设置初始资金 1000w
    cerebro.broker.setcash(10_000_000.0)
    # 每次交易的股票数量
    cerebro.addsizer(bt.sizers.FixedSize, stake=100000)
    # 交易手续费设置
    cerebro.broker.setcommission(commission=0.00025)
    # 为Cerebro引擎添加策略
    cerebro.addstrategy(Strategy001)
    # 获取历史交易数据
    format_data = query_stock_rate("300059", "20210101")
    cerebro.adddata(format_data)
    # 引擎运行前打印期出资金
    start_cash = cerebro.broker.getvalue()

    cerebro.run()
    # 引擎运行后打期末资金
    print('组合期初资金: %.2f' % start_cash)
    print('组合期末资金: %.2f' % cerebro.broker.getvalue())
    # 绘图
    # volup voldown 设置成交量在行情上涨和下跌情况下的颜色
    # barup bardown 设置蜡烛图上涨和下跌的颜色
    cerebro.plot(style='candel', iplot=False, barup='#ff9896', bardown='#98df8a',
                 volup='#ff9896', voldown='#98df8a')
