from src import spider
import json
import time
import os

# 将结果输出到jd.txt/json
current_path = os.path.dirname(__file__)
file = open(current_path+'/data/jd.txt', 'w', encoding='utf-8')
jsonFile = open(current_path+'/data/jd.json', 'w', encoding='utf-8')

number = 1  # 序号
typeMapping = dict()  # 类别映射
jsonData = {'jd': []}  # json数据


# 关闭文件
def fileClose():
    file.close()
    jsonFile.close()


# 构建类别映射表
def mapping():
    typeMapping[12762] = '房产'
    typeMapping[12767] = '债权'
    typeMapping[12766] = '股权'
    typeMapping[12763] = '交通运输'
    typeMapping[12764] = '土地林权'
    typeMapping[12765] = '机械设备'
    typeMapping[12769] = '无形资产'
    typeMapping[12768] = '知识产权'
    typeMapping[21440] = '库存物资'
    typeMapping[13129] = '其它资产'
    typeMapping[21439] = '租赁/经营权'


# 判断是否含有汉字
def hasChinese(s):
    for c in s:
        if '\u4e00' <= c <= '\u9fa5':
            return True
    return False


# 主进程
def main():
    mapping()

    pages = 4  # 网页共有4页
    url = 'https://auction.jd.com/getAssetsList.html?childrenCateId=12762&provinceId=12&limit=40&page='
    fix = '&callback=axiosJsonpCallback6&_=1598077141286'

    for i in range(pages):
        getData(url + str(i + 1) + fix)

    json.dump(jsonData, jsonFile, indent=2, sort_keys=True, ensure_ascii=False)


# 抓取每页数据
def getData(url):
    res = spider.getHtml(url)
    text = res.text.split('(')[1].replace(')', '')
    jsonObj = json.loads(text)['ls']

    for item in jsonObj:
        writeTxt(item)
        writeJson(item)


# 写入txt数据
def writeTxt(data):
    global number

    # 2018年之前的忽略
    secs = float(data['endTime'])
    timeArray = time.localtime(secs / 1000)
    if timeArray.tm_year < 2018:
        return

    file.write(str(number) + '.')
    file.write(data['title'] + '\n')
    file.write('当前价：' + str(data['currentPrice']) + '\n')
    file.write('保证金：' + str(data['ensurePrice']) + '\n')
    file.write('加价幅度：' + str(data['priceLowerOffset']) + '\n')
    file.write('出价次数：' + str(data['bidCount']) + '\n')
    # file.write('类别：' + typeMapping[data['productCateId']] + '\n')
    file.write('城市：' + data['city'] + '\n')
    publisher = data['publisher']
    if hasChinese(publisher):
        file.write('送拍机构：' + publisher + '\n\n')
    else:
        file.write('送拍机构：未知\n\n')

    print(number)
    number = number + 1


def writeJson(data):
    # 2018年之前的忽略
    secs = float(data['endTime'])
    timeArray = time.localtime(secs / 1000)
    if timeArray.tm_year < 2018:
        return

    jsonObj = dict()

    jsonObj['title'] = data['title']
    jsonObj['currentPrice'] = data['currentPrice']
    jsonObj['ensurePrice'] = data['ensurePrice']
    jsonObj['priceLowerOffset'] = data['priceLowerOffset']
    jsonObj['bidCount'] = data['bidCount']
    # jsonObj['type'] = typeMapping[data['productCateId']]
    jsonObj['city'] = data['city']
    publisher = data['publisher']
    if hasChinese(publisher):
        jsonObj['publisher'] = publisher
    else:
        jsonObj['publisher'] = '未知'

    jsonData['jd'].append(jsonObj)
