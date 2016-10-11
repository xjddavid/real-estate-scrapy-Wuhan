# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy.item import Item, Field 
class Room(Item):
    building_no = Field() #栋号
    unit = Field() #单元号
    floor = Field() #层数
    room_no = Field() #房间号

