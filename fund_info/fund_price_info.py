import requests
# 使用BeautifulSoup解析网页
from bs4 import BeautifulSoup


# 获取基金的价格信息
def query_fund_price(code):
    response = requests.get("http://fund.eastmoney.com/{}.html".format(code))
    response.encoding = "UTF-8"
    resp = response.text
    soup = BeautifulSoup(resp, 'lxml')
    # 基金净值信息
    price_dl = soup.find("dl", class_="dataItem02")
    p_text = price_dl.find("p")
    price_spans = price_dl.find("dd", class_="dataNums").find_all("span")
    # 更新日期
    update_date = p_text.get_text().replace("单位净值 (", "").replace(")", "")
    price = price_spans[0].get_text()
    price_percent = price_spans[1].get_text().replace("%", "")

    # 基金规模信息
    fund_table = soup.find("div", class_="infoOfFund")
    fund_size_td = fund_table.find_all("td")[1]
    scale_td = fund_size_td.get_text().replace("基金规模：", "")
    fund_size = scale_td.split("亿元")[0]

    price_info = "code {} price {} percent {} fund_size {} update_date {}"\
        .format(code, price, price_percent, fund_size, update_date)
    # print(price_info)
    return update_date, price, price_percent, fund_size


if __name__ == '__main__':
    print("start analyze !")
    query_fund_price("159779")
