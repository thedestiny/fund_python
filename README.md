# fund_python
use python script gather fund basic information and rate information


159766

159869

##### 文件说明

``` 
# 文件目录说明
stock_info 股票信息获取相关脚本
  - stock_k_line.py  股票k线数据获取
  - stock_north_hold.py 股票北上资金持仓情况
  - stock_list_info.py 获取股票信息列表和股票基本信息
  
fund_info 基金信息获取相关脚本
  - db_executor.py 数据库操作相关脚本
  - etf_rate_info.py 场内etf信息获取
  - fund_basic.py 基金基本信息获取
  - fund_list.py 基金列表新获取
  - fund_price_info.py 基金价格信息获取
  - fund_rate_info.py 基金变动信息获取
  - update_fund_info.py 更新基金信息，存入数据库

stock_model 股票模型相关脚本
  - stock_model_draw.py 股票技术指标绘制图形
  - stock_model_draw_1.py 股票技术指标绘制图形1
  - stock_model_support.py 加托模型数据计算
  
fund_model 基金模型相关脚本  
  - fund_trend.py 基金趋势模型
  
trade 交易回测模型
  - trade_001.py 交易模型回测01
  
```


```
python 概率统计
https://mp.weixin.qq.com/s/3vJzhXkKyQ15_mdpStVG5Q

# 反转索引
data = st_line.query_stock_info("603628")
print(data)
tmi = data.set_index(data["Date"], drop=True)
print(tmi)
tmi.index = range(len(tmi))
tmi = tmi.reset_index()
# df[reversed(df.columns)] 反转列名
# reversed方法时，索引不能重复
print(tmi)
tmp = data.set_index("Date", drop=True)
print(tmp)
tpm = tmp.reindex(reversed(tmp.index))
print(tpm)
dt = data.loc[::-1]
print(dt)
handle_stock("603628	清源股份")
    
```




```


```

fidder 手机抓包
https://blog.csdn.net/wxyczhyza/article/details/129128004

```






```