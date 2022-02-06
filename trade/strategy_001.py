import datetime  #
import os.path  # 路径管理
import sys  # 获取当前运行脚本的路径 (in argv[0])

# 导入backtrader框架
import backtrader as bt


# 创建策略继承bt.Strategy
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        # 记录策略的执行日志
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 保存收盘价的引用
        self.dataclose = self.datas[0].close

    def next(self):
        # 记录收盘价
        self.log('Close, %.2f' % self.dataclose[0])
        # 今天的收盘价 < 昨天收盘价
        if self.dataclose[0] < self.dataclose[-1]:
            # 昨天收盘价 < 前天的收盘价
            if self.dataclose[-1] < self.dataclose[-2]:
                # 买入
                self.log('买入, %.2f' % self.dataclose[0])
                self.buy()
