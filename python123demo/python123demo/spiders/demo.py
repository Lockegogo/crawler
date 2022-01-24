import scrapy

class DemoSpider(scrapy.Spider):
    name = 'demo'
    #allowed_domains = ['python123.io']
    start_urls = ['http://python123.io/ws/demo.html']

    def parse(self, response):
        """
        self 是面向对象类所属关系的标记
        response 是从网页内容所存储或对应的对象
        """
        fname = response.url.split('/')[-1]
        with open(fname, 'wb')  as f:
            f.write(response.body)
        self.log('Save file %s.' % name)