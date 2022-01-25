import scrapy
import re

class StocksSpider(scrapy.Spider):
    name = 'stocks'
    start_urls = ['http://quote.eastmoney.com/stock_list.html']

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            try:
                stock = re.findall(r"[s][hz]\d{6}", href)[0]
                # e.g. https://gu.qq.com/sh603102/gp
                url = 'http://gu.qq.com/' + stock + '/gp'
                # 重新提交 URL
                yield scrapy.Request(url, callback=self.parse_stock)
            except:
                continue

    def parse_stock(self, response):
        infoDict = {}
        # 找到属性为 title_bg 的区域
        stockName = response.css('.title_bg')
        stockInfo = response.css('.col-2.fr')
        # 然后在这一个区域中进一步检索 col-1-1 并且把相关的字符串提取出来
        # e.g. N 百合
        name = stockName.css('.col-1-1').extract()[0]
        # e.g. 603102.SH
        code = stockName.css('.col-1-2').extract()[0]
        # 进一步搜索名称为 li 的标签
        # 注意搜索属性前面有 ., 而搜索名称没有
        info = stockInfo.css('li').extract()
        for i in info[:13]:
            key = re.findall('>.*?<', i)[1][1:-1]
            key = key.replace('\u2003', '')
            key = key.replace('\xa0', '')
            try:
                val = re.findall('>.*?<', i)[3][1:-1]
            except:
                val = '--'
            infoDict[key] = val
        # 注意 update 和直接赋值都能达到改变字典的目的
        # 但是 update 的实现方式是遍历字典赋值，性能比直接赋值要低
        # 只有在设计两个字典合并的操作，使用 dict1.update(dict2)
        infoDict.update({' 股票名称': re.findall('\>.*\<', name)[0][1:-1] + \
                                 re.findall('\>.*\<', code)[0][1:-1]})
        yield infoDict
