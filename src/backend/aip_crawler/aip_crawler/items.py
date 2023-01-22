# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AIPPageItem(scrapy.Item):
    airport = scrapy.Field()
    filename = scrapy.Field()
    src = scrapy.Field()
