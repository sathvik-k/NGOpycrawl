from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from scrapy.crawler import CrawlerProcess

NGOGlobalItems = []
class MyItem(Item):
    url= Field()


class LinkSpider(CrawlSpider):
    name = 'ngoLink'
    allowed_domains = ['afcfoundation.org']
    start_urls = ['http://www.afcfoundation.org']

    rules = (Rule(LinkExtractor(), callback='parse_url'), )

    def parse_url(self, response):

        NGOGlobalItems.append(response.url)
        # invoke your parsing code on response




process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(LinkSpider)
process.crawl
process.start() # the script will block here until the crawling is finished

"""
   myspider = MySpider()
   MySpider.name = ' alsdads'
   myspider.alloed_urls = req.urls
   myspider,start_urls = req.start_urls

   scapyapi.startspider(myspider)
   return json.dumps(addresses)
  """
