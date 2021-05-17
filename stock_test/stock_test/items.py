# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StockTestItem(scrapy.Item):
    # define the fields for your item here like:
    stock_code = scrapy.Field()
    date = scrapy.Field()
    deal_time = scrapy.Field()
    deal_price = scrapy.Field()
    increment = scrapy.Field()
    price_variation = scrapy.Field()
    shares = scrapy.Field()
    volume = scrapy.Field()
    status = scrapy.Field()


