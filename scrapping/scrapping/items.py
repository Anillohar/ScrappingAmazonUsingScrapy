# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
class ScrappingItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    quantity = scrapy.Field()
	price = scrapy.Field()
	mrp = scrapy.Field()
	image = scrapy.Field()
	image_urls = scrapy.Field()
	anything = scrapy.Field()
