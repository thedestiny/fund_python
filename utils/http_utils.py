import requests
import json
import datetime as dt

# http 请求工具类

class http_utils(object):

    def __init__(self, server):
        self.session = requests.session()
        self.server = server
        self.header = {
            "content-type": "application/json"
        }

    def print_datetime(self):
        date_str = dt.datetime.now().strftime("%Y%m%d%H%M%S%s")
        print("date time is : " + date_str)

    def post_invoke(self, uri, data):
        self.print_datetime()
        print("data is ", data.encode())
        resp = self.session.post(self.server + uri, headers=self.header, data=data.encode())
        print("result is ", resp.text)
        return resp.text

    def get_invoke(self, uri, data):
        pass


if __name__ == '__main__':

    print("http 工具类")

    hpu = http_utils("http://localhost:9098")

    dat = {
        "username": "李晓明",
        "password": "123456"
    }

    resp = hpu.post_invoke("/api/index", json.dumps(dat, ensure_ascii=False))
    print(resp)
