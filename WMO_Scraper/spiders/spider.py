# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 22:26:46 2022

@author: jonat
"""
import scrapy
import json
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector

import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, SelectJmes

from WMO_Scraper.items import WmoScraperItem
from lxml import etree
import lxml.etree
import lxml.html

class OSCARSpider(scrapy.Spider):
    name = "wmo_oscar"
    start_urls = ['https://space.oscar.wmo.int/variables']
    allowed_domains = ['space.oscar.wmo.int']
    wmo_items = {
        'Id' : 'Id',
        'VarName' : 'VarName',
        'Domain' : 'Domain',
        'MeasUnit' : 'MeasUnit',
        'Defin' : 'Defin',
        'UncertUnit' : 'UncertUnit',
        'ReqApp' : 'ReqApp',
        'Layers' : 'Layers',
    }
    
    custom_settings = {
        "FEEDS": {"output.csv":{"format":"csv"}},
    }

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "referer": "https://space.oscar.wmo.int/variables",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        }
    
    def parse(self, response):
        base_url_displaystart = "https://space.oscar.wmo.int/variables?subdomains=&applicationareas=&layers=&themes=&iDisplayStart="
        base_url_draw = "&iDisplayLength=50&iSortCol_0=1&sSortDir_0=asc&draw="
        draw = 0
        for x in range(0,327,50):
            url = base_url_displaystart+str(x)+base_url_draw+str(draw)
            request = scrapy.Request(url, callback=self.parse_api, headers=self.headers)
            yield request
        
    def parse_api(self,response):
        #htmlText = json.loads(response.text)['aaData']
        #print(htmlText[0][1])
        #resultPage = etree.HTML(htmlText[0][1])
        #lxml.etree.strip_elements(resultPage)
        #print(lxml.html.tostring(resultPage, method="text"))
        #print(resultPage.xpath('//aaData'))
        ##rows = table.xpath('//tr')
        ##row = rows[0].extract()
        ##print("bruh", row.xpath('td//text()')[0].extract())
        raw_data = response.body    ##Returns string
        data = json.loads(raw_data) ##JSON object
        reqs = {}
        #for dat in data['aaData']:
            #result_reqid = dat[0];
            #reqs["Id"] = result_reqid
            #yield reqs
        for dat in data['aaData']:
            v_id = dat[0]
            v_name = dat[1]
            v_domain = dat[2]
            v_measunit = dat[3]
            v_defin = dat[4]
            v_uncerunit = dat[5]
            v_reqapp = dat[6]
            v_layers = dat[7]
            yield WmoScraperItem(Id=v_id, VarName=v_name, Domain=v_domain, MeasUnit=v_measunit, Defin = v_defin, UncertUnit = v_uncerunit, ReqApp = v_reqapp, Layers=v_layers)
