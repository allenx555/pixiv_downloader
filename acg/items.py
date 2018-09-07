# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AcgItem(scrapy.Item):
    image_urls = scrapy.Field()
    image_referer = scrapy.Field()
    image_path = scrapy.Field()
    image_form = scrapy.Field()
    image_name = scrapy.Field()
    drawer_name = scrapy.Field()
    drawer_id = scrapy.Field()
