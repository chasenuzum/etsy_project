#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 01:49:47 2019

@author: chasenuzum
"""

import scrapy

class EtsySpider(scrapy.Spider):
    name = "etsy_spider"
    start_urls = [
            'https://www.etsy.com/c/books-movies-and-music/music/musical-instruments?ref=catnav-11049'
            ] #Bionicle url
    with open('myresults.csv', 'w') as f:
        f.write("URL, SELLERNAME, SELLERURL, ITEM, PRICE, BESTSELLER, FREESHIPPING\n") #writing to csv with these columns
    
    def parse(self, response):
        with open('myresults.csv', 'a') as f:
            ITEM_SELECTOR = ".set"
            for brickset in response.xpath(ITEM_SELECTOR): #run through brickset source, ".set"
                
                #URL = response.request.url
                #SELLERNAME =
                #SELLERURL =
                ITEM= '//*[(@id = "reorderable-listing-results")]//*[contains(concat( " ", @class, " " ), concat( " ", "text-body", " " ))]'
                PRICE= '//span[@id='listing-price']/span/span[@class='currency-value']/text()'
                #BESTSELLER =  "//span[@class='review-rating']/meta[@itemprop='rating']/@content")
                #FREESHIPPING =
                #result = str(brickset.xpath(URL).extract_first()) + "," #no commas in all data except notes sections below
                #result += str(brickset.xpath(SELLERNAME).extract_first()) + "," #need to find
                #result += str(brickset.xpath(SELLERURL).extract_first()) + "," #replace | with whitespace
                result = str(brickset.xpath(ITEM).extract_first()) + "," #replace c with whitespace
                result += str(brickset.xpath(PRICE).extract_first()) + "\n"
                #result += str(brickset.xpath(BESTSELLER).extract_first()) + "," need to find
                #result += str(brickset.xpath(FREESHIPPING).extract_first()) + "\n"#(',', '') + "," need to find
                        
                f.write(result) #write to csv
                
                NEXT_PAGE_SELECTOR = '.next a ::attr(href)' #need to find
                next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
                if next_page:
                    yield scrapy.Request(
                        response.urljoin(next_page),
                        callback=self.parse
                    )
                    