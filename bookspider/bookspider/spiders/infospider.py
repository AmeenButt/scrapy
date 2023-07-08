import scrapy
from bookspider.items import BookItems
import random
from urllib.parse import urlencode




API_KEY = '8b570a1a-5b2b-4e21-a892-5b8f5a326cbe'

#def get_proxy_url(url):
 #   payload = {'Api_key': API_KEY, 'url': url}
  #  proxy_url = 'https://proxy.scrapeops.io/v1/' + urlencode(payload)
   # return proxy_url


class InfospiderSpider(scrapy.Spider):
    name = "infospider"
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']
    item_count = 1


    custom_settings = {
        'FEEDS' : {
        'booksdata.json': {'format': 'json', 'overwrite':True },
        }
    }

   #def start_requests(self):
      #  yield scrapy.Request(url=get_proxy_url(url), callback=self.parse)



    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield scrapy.Request(url =book_url, callback=self.parse_book_page)


        #next page
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield scrapy.Request(url =next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        table_rows = response.css('table tr')
        book_item = BookItems()

        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        book_item['title'] = response.css('div h1::text').get()
        book_item['price'] = response.css('.product_main .price_color::text').get()
        book_item['star_rating'] = response.css('p.star-rating').attrib['class']
        book_item['product_type'] = table_rows[1].css('td ::text').get()
        book_item['price_excl_tax'] = table_rows[2].css('td ::text').get()
        book_item['price_incl_tax'] = table_rows[3].css('td ::text').get()
        book_item['availability'] = table_rows[5].css('td ::text').get()

        yield book_item

    def closed(self, reason):
        self.logger.info("Total items scraped: %s", self.item_count)