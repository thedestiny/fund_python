import stock_info.stock_k_line as sk_line
import pandas as pd
import requests
import json
import numpy as np
import dateutil.relativedelta as dr
import sys
import datetime


class stock_model(object):

    def __init__(self, code):

        self.code = code
        self.count = 0
        # 阈值
        self.threshold = -0.04
        # 回顾周期
        self.period = 30
        # 周期
        self.type = "d"
        # 类型 etf stock


    # 参数请求组装
    def compose_params(self, code, start="20200101", end="20300101", klt="101"):
        tmp = "0." + code
        if code.startswith("6"):
            tmp = "1." + code
        prms = {
            "secid": tmp,
            "ut": "fa5fd1943c7b386f172d6893dbfba10b",
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": klt,
            "fqt": "1",
            "beg": start,
            "end": end,
            "lmt": "1000000",
        }
        result = ""
        for key, val in prms.items():
            result = result + key + "=" + val + "&"
        result = result[:-1]
        # print(result)
        return result

    # 查询数据
    def query_k_line(self, code, start="20200101", end="20300101", klt="101"):
        params = self.compose_params(code, start, end, klt)
        server = "http://54.push2his.eastmoney.com/api/qt/stock/kline/get"
        url = server + "?" + params
        resp = requests.get(url).text
        json_body = json.loads(resp)
        # 解析数据结果可以得到k线数据在 data-kline节点下
        json_data = json_body["data"]
        kline_data = json_data["klines"]
        # 创建一个对象 PrettyTable 用于打印输出结果
        # bt = PrettyTable()
        # title_list = ["时间", "开盘", "收盘", "最高", "最低", "成交量", "成交额", "振幅", "涨跌幅", "涨跌额", "换手率"]
        # bt.field_names = title_list
        # for node in kline_data:
        #     arr = node.split(",")
        #     # 将表格内容放置在 bt 中
        #     bt.add_row(arr)
        # # print(bt)
        # # print(kline_data)
        return kline_data

    def query_stock_pandas(self, code, sat="20200101"):

        line_list = self.query_k_line(code, sat)

        date_list, open_list, close_list, high_list, low_list, rate_list = [], [], [], [], [], []
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
            rate_list.append(float(arr[8]))
        # 组装 dataframe 数据
        data = pd.DataFrame({
            "date": date_list,
            "high": high_list,
            "low": low_list,
            "open": open_list,
            "close": close_list,
            "volume": vol_list,
            "amount": amt_list,
            "rate": rate_list
        })
        return data

    def read_data(self, stat="20200101"):

        pands = self.query_stock_pandas(self.code, stat)
        pands["yes_close"] = pands.close.shift(1)

        yes_c = pands["close"][0] / (1 + pands["rate"][0])
        pands["yes_close"][0] = round(yes_c, 3)

        pands["low_rate"] = pands["low"] / pands["yes_close"] - 1
        pands.set_index("date", inplace=True)
        # print(yes_c)

        self.pd_list = pands
        # print(pands)

    def push_date(self, dat, days_num):

        date = datetime.datetime.strptime(dat, "%Y-%m-%d")
        d = date + dr.relativedelta(days=days_num)
        for p in range(30):
            tmp = d + dr.relativedelta(days=p)
            tp = tmp.strftime('%Y-%m-%d')
            if tp in self.pd_list.index:
                # d + dr.relativedelta(days=p)
                return tp

    def handle_null(self, dat_list):
        result_list = []
        for ne in dat_list:
            if ne:
                result_list.append(ne)
        return result_list

    def run_model(self):
        # 读取数据
        self.read_data()
        # 复制数据
        ball_df = self.pd_list.copy()

        # 计算数据
        result = pd.DataFrame()

        for t in range(len(ball_df)):
            start_date = ball_df.index[t]
            low_rate = ball_df['low_rate'].loc[start_date]
            # 期初价格
            # 跌幅大于设定的阈值
            if low_rate < self.threshold:
                self.count = self.count + 1
                buy_price = round(ball_df['yes_close'].loc[start_date] * (1 + self.threshold), 4)
                print("\n{} trigger buy {} price {} \n".format(self.count, start_date, buy_price))

                obs_date = [self.push_date(start_date, i) for i in range(1, int(self.period * 2))]

                obs_date = self.handle_null(obs_date)
                obs_date = sorted(list(set(obs_date)))
                obs_date = obs_date[0: self.period]

                dat_list = [0 for _ in range(self.period + 2)]
                dat_list[0] = buy_price
                cal_num = 1
                for ind in ball_df.loc[start_date: obs_date[-1]].index:
                    px = ball_df['close'].loc[ind]
                    interest = round(100 * (px - buy_price) / buy_price, 3)
                    print("day {} hold {} and {}".format(ind, cal_num, interest))
                    dat_list[cal_num] = interest
                    cal_num = cal_num + 1

                # if len(dat_list) >= self.period:
                result[start_date] = dat_list

        print(result)
        verse = result.T
        file_name = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
        verse.to_excel("./data_{}_{}.xlsx".format(self.code, file_name))
        print(verse)


if __name__ == '__main__':
    print("start stock select !")
    # 002032
    stm = stock_model("000333")
    stm.run_model()
