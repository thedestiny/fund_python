import requests
# 使用BeautifulSoup解析网页
from bs4 import BeautifulSoup
import uuid

# 查询图片地址
def query_image(url, page=1):

    if page > 1:
        url = url + "index_{}".format(page) + ".html"
        # https://pic.netbian.com/4kfengjing/index_2.html
    print("start -> " + url)
    body = requests.get(url).text
    soup = BeautifulSoup(body, 'lxml')
    a_list = soup.find_all("a")
    for node in a_list:

        href_url = node.get("href")
        if href_url and "tupian" in href_url:
            # print(href_url)
            detail_body = requests.get("https://pic.netbian.com/" + href_url).text
            soup = BeautifulSoup(detail_body, 'lxml')
            actual_url = soup.find("a", id="img")
            # print(actual_url)
            # 从图片地址下载数据

            a_url = actual_url.find_all("img")[0].get("src")
            print(a_url)
            image = requests.get("https://pic.netbian.com/" + a_url)
            # 在目标路径创建相应文件
            # image_name = uuid.uuid1().hex
            image_name = a_url.split("-")[1]
            f = open('./images/' + image_name, 'wb')
            # 将下载到的图片数据写入文件
            f.write(image.content)
            f.close()


if __name__ == '__main__':
    # https://pic.netbian.com/4kmeinv/
    # https://pic.netbian.com/4kfengjing/
    # https://pic.netbian.com/4kyingshi/
    # https://pic.netbian.com/4krenwu/
    # https://pic.netbian.com/4kdongman/
    # https://pic.netbian.com/4kyouxi/

    image_list = [""]
    url = "https://pic.netbian.com/4kmeinv/"
    for node in range(2, 10):
       query_image(url, node)

