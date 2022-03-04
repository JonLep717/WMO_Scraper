# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class WmoScraperItem(scrapy.Item):
    Id = Field()
    VarName = Field()
    Domain = Field()
    MeasUnit = Field()
    Defin = Field()
    UncertUnit = Field()
    ReqApp = Field()
    Layers = Field()
