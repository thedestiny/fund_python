import requests
import demjson

invoke_url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=fb&sc=clrq&st=desc&pi=1&pn=5000"
headers = {
    'Host': 'fund.eastmoney.com',
    'Referer': 'http://fund.eastmoney.com/data/fbsfundranking.html'
}


def query_etf_rate_info():
    response = requests.get(invoke_url, headers=headers)
    print(response.text)
    body_data = response.text.replace("var rankData = ", "")
    print(body_data)
    resp_body = demjson.decode(body_data)
    print(resp_body)


if __name__ == '__main__':
    print("start etf analyze !")
    query_etf_rate_info()
