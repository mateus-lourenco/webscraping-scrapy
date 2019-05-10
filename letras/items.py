# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class Musica(Item):    
    artista = Field()
    album = Field()
    titulo = Field()
    compositor = Field()
    letra = Field()
