import requests
from bs4 import BeautifulSoup
import random
import time

# 构造请求头，模拟浏览器访问
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; '
                         'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}


# 爬取对应url内容并返回soup对象
def getSoup(url):
    # 随机睡眠1——3s防止反爬
    time.sleep(random.randint(1, 3))

    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')

    return soup

def getHtml(url):
    # 随机睡眠1——3s防止反爬
    time.sleep(random.randint(1, 3))

    html = requests.get(url, headers=headers)

    return html
