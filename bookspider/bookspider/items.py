# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookspiderItems(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class BookItems(scrapy.Item):
    category = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    star_rating = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    availability = scrapy.Field()


