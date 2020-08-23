# 拍卖信息抓取

### 抓取链接
- [京东资产拍卖](https://auction.jd.com/zichan.html/)
- [淘宝资产拍卖](https://zc-paimai.taobao.com/zc/index.htm?scm=20140647.sem.pm.wushuang5473)

### 输出
- 输出文件位于`src/data/`，包含`txt`与`json`两种格式
- 京东抓取数据如下
```json
{
      "bidCount":         "竞标人数",
      "city":             "标物所在城市",
      "currentPrice":     "当前标价",
      "ensurePrice":      "保证金",
      "priceLowerOffset": "加价幅度",
      "publisher":        "送标机构",
      "title":            "标物名"
}
```
- 淘宝抓取数据如下
```json
{
      "bidCount":         "竞标人数",
      "city":             "标物所在城市",
      "currentPrice":     "当前标价",
      "ensurePrice":      "保证金",
      "marketPrice":      "评估/市场价",
      "priceLowerOffset": "加价幅度",
      "title":            "标物名"
}
```

### 配置
- Python 3.8
- pip 20.2.2

### 包配置
```
pip install requests
pip install bs4
```

### 注意事项
- 请在 JD.py line 49 修改京东爬取页数
- 请在 TB.py line 19 修改京东爬取页数
