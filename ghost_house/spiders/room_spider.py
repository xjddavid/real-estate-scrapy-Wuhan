# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from scrapy.spider import BaseSpider
from scrapy.http import HtmlResponse
import urllib
import string
from ghost_house.items import Room
import re


class RoomSpider(BaseSpider):
    name = "room"
    allowed_domains = ["http://119.97.201.28/"]
    start_urls = [
        "http://119.97.201.28:8087/4.asp?DengJh=%BA%FE1400329",
    ]
    prefix_url = "http://119.97.201.28:8087/"

    def parse_ghost_room(self, response):
        ghost_rooms = []
        for tr in response.xpath('//table/tbody/tr[@height="25"]').extract():
            td_pattern = re.compile(r"<td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>(.*)</tr>")
            tds = td_pattern.search(tr).groups()
            building_no = tds[0]
            unit = tds[1]
            floor = tds[2]
            room_pattern = re.compile(r'<td bgcolor="(.*?)">\D*(\d*)\D*')
            for td in tds[3].split('</td>'):
                if td and td != "<td>-": #special data
                    rooms = room_pattern.search(td).groups()
                    if rooms[0] == "#CCFFFF": # the magic color
                        item = Room()
                        item['building_no'] = building_no
                        item['unit'] = unicode(unit)
                        item['floor'] = unicode(floor)
                        item['room_no'] = unicode(rooms[1])
                        ghost_rooms.append(item)
        return ghost_rooms

    def parse(self, response):
        items = []
        all_urls = response.xpath('//td/a/@href').extract()[1:]
        buildings = response.css('span::text').extract()
        for url in all_urls:
            child_url = self.prefix_url+urllib.quote(url.encode('gb2312'),safe=string.printable)
            # if child_url == "http://119.97.201.28:8087/5.asp?DengJh=%CF%C400020&HouseDengjh=%CF%C40001769":
            items.extend([scrapy.Request(child_url, callback=self.parse_ghost_room, dont_filter=True)])
        return items

    