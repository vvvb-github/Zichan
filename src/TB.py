from src import spider
import time
import json
import bs4
import os


# 将结果输出到jd.txt/json
current_path = os.path.dirname(__file__)
file = open(current_path+'/data/tb.txt', 'w', encoding='utf-8')
jsonFile = open(current_path+'/data/tb.json', 'w', encoding='utf-8')

number = 1  # 序号
jsonData = {'tb': []}  # json数据


# 关闭文件
def closeFile():
    file.close()
    jsonFile.close()


# 主进程
def main():
    pages = 2  # 页数，网页共含有150页，此处抓取2页作为测试
    for i in range(pages):
        getData(i + 1)

    json.dump(jsonData, jsonFile, indent=2, sort_keys=True, ensure_ascii=False)


# 抓取某页数据
def getData(page):
    url = 'https://zc-paimai.taobao.com/zc_item_list.htm?auction_source=2&front_category=56950002&province=%BD%AD%CB' \
          '%D5&st_param=-1&auction_start_seg=-1&page= '

    soup = spider.getSoup(url + str(page))
    jsonStr = soup.select('#sf-item-list-data')[0].contents[0]
    dataList = json.loads(jsonStr)['data']
    itemUrl = 'https://zc-item.taobao.com/auction/'
    fix = '.htm?spm=a219w.7474998.paiList.1.3168211dKbfQOW'

    for item in dataList:
        getDetail(itemUrl + str(item['id']) + fix)


# 抓取链接对应资产相关数据
def getDetail(url):
    global number

    soup = spider.getSoup(url)

    # 判断结束时间，2018年以前的忽略
    secs = float(soup.select('#sf-countdown')[0].get('data-end'))
    timeArray = time.localtime(secs / 1000)
    if timeArray.tm_year < 2018:
        return

    # 抽取数据
    priceLowerOffset = 0.0
    ensurePrice = 0.0
    marketPrice = 0.0
    trs = soup.select('#J_HoverShow > tr')
    for tr in trs:
        for td in tr.select('td'):
            info = td.select('span.pay-mark.i-b')[0].get_text()
            if info == '评 估 价' or info == '市 场 价':
                marketPrice = float(td.select('span.pay-price > span.J_Price')[0].get_text().replace(',',''))
            elif info == '保 证 金':
                ensurePrice = float(td.select('span.pay-price > span.J_Price')[0].get_text().replace(',',''))
            elif info == '加价幅度':
                priceLowerOffset = float(td.select('span.pay-price > span.J_Price')[0].get_text().replace(',',''))

    currentPrice = float(soup.select('#sf-price > div > p.i-info-wrap.i-left > span > em')[0].get_text().replace(',', ''))
    title = soup.select('#page > div:nth-child(7) > div > div > h1')[0].contents[2].strip()
    bidCount = int(soup.select('#page > div:nth-child(7) > div > div > div.pm-main-l.auction-interaction > '
                               'div.pm-remind > span.pm-apply.i-b > em')[0].get_text())
    # publisher = soup.select('#J_desc > table > tbody > tr:nth-child(5) > td:nth-child(2) > p > span')
    # if len(publisher) > 0:
    #     publisher = publisher[0].get_text()
    # else:
    #     publisher = '未知'
    city = soup.select('#itemAddress')[0].get_text().split(' ')[1]

    # 写入txt
    file.write(str(number) + '.')
    file.write(title + '\n')
    file.write('当前价：' + str(currentPrice) + '\n')
    file.write('保证金：' + str(ensurePrice) + '\n')
    file.write('加价幅度：' + str(priceLowerOffset) + '\n')
    file.write('评估/市场价：' + str(marketPrice) + '\n')
    file.write('出价次数：' + str(bidCount) + '\n')
    file.write('城市：' + city + '\n\n')
    # file.write('送拍机构' + publisher + '\n\n')

    print('tb:' + str(number))
    number = number + 1

    # 写入json
    jsonObj = dict()
    jsonObj['title'] = title
    jsonObj['currentPrice'] = currentPrice
    jsonObj['ensurePrice'] = ensurePrice
    jsonObj['priceLowerOffset'] = priceLowerOffset
    jsonObj['marketPrice'] = marketPrice
    jsonObj['bidCount'] = bidCount
    jsonObj['city'] = city
    # jsonObj['publisher'] = publisher

    jsonData['tb'].append(jsonObj)
