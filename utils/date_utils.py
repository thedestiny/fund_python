import dateutil.relativedelta as dr
import datetime as dt


def format_dat():
    date_str = dt.datetime.now().strftime("%Y%m%d%H%M%S%s")
    print(date_str)
    return date_str
#
obs_date = [2, 2, 3, 4, ]
dd = obs_date[:-1]
print(dd)

start = dt.date(2020, 1, 15)
for i in range(3):
    print("is is {}".format(i))

# 间隔 1 天
dd = start + dr.relativedelta(days=1)
date_list = []
for nd in range(20, 30):
    dd = start + dr.relativedelta(days=nd)
    date_list.append(dd)

date1_list = []
for nd in range(10, 20):
    dd = start + dr.relativedelta(days=nd)
    if dd not in date_list:
        date_list.append(dd)
    date1_list.append(dd)

date_list.sort()
sorted(date_list, reverse=False)
print(dd)
print(date_list)

if __name__ == '__main__':


    print("date 工具类")