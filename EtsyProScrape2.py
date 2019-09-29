#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 00:00:59 2019

@author: chasenuzum
"""
#RUN THIS SCRAPY FIRST; IT WILL RETRIEVE THE UNIQUE SELLER URLS FOR EtsyProScrapeSell.py
import scrapy

filename = 'etsydata.csv'

class EtsySpider(scrapy.Spider):
    name = "etsy_spider"
    DOWNLOAD_DELAY = 0 #No delay between page scapes; Etsy did not close spider for requests
    DOWNLOAD_TIMEOUT = 200 #Makes scrapy continue for time past default timeout
    start_urls = [
            'https://www.etsy.com/c/books-movies-and-music/music/musical-instruments?ref=pagination&page=1',
            'https://www.etsy.com/c/books-movies-and-music/music/instrument-straps?ref=pagination&page=1',
            'https://www.etsy.com/c/books-movies-and-music/music/recorded-audio?ref=pagination&page=1',
            'https://www.etsy.com/c/books-movies-and-music/music/sheet-music?ref=pagination&page=1'
            
            ] #load in subcatergory url start pages
    with open(filename, 'w') as f:
        f.write('name,price,rating,free_shipping,best_seller,sellername,sellername2,sellerurl,sellerurl2,comments,location\n')
        #Write in csv with no spaces in column name; so can be used for analysis/easy cleaning
                
    def parse(self, response): #define parse method

        listings = [] #list for all urls from selected page
        for i in response.xpath("//a/@href"): 
            if '/listing/' in i.get(): #get all listings from start page
                listings.append(i.get()) #append to listing
        for j in listings:
            yield scrapy.Request(j, callback=self.parse_item) #collect nodes from parse_item
        
        #NEXT_PAGE_SELECTOR = "//div/nav/ul[@class='btn-group-lg list-unstyled text-left']/li[@class='btn btn-list-item btn-secondary btn-group-item-lg'][2]/a/@href" #next page step path from class, still works
        NEXT_PAGE_SELECTOR = "//div/nav/ul[@class='btn-group-lg list-unstyled text-left']/li[@class='btn btn-list-item btn-secondary btn-group-item-lg'][last()]/a/@href" #Next page xpath
        next_page = response.xpath(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                    response.urljoin(next_page), #call next page xpath
                    callback=self.parse #call back first parse method
                    )
       

    def parse_item(self, response): #parse_item after parse method; selects attributes
        with open(filename, 'a') as f:
            name = "//div[@class='listing-page-title-component']/h1/text()" #xpaths need to be correct and might be updated later
            price = "//div/p/span[@class='text-largest strong override-listing-price']/text()"
            rating = "//div[@id='listing-page-cart']/div[@class='ui-toolkit']/div/div/a/div/span/input[@type='hidden'][1]/@value"
            free_shipping = '//div[@class = "text-gray-lighter text-body mt-xs-1 mb-xs-1"]/text()'
            best_seller = '//div[@class = "ui-toolkit"]/span/span[@class = "text-gray display-inline-block vertical-align-middle"]/text()'
            sellername = "//div[@class='text-center']/a/p[@class = 'text-title-smaller']/text()"
            sellerurl = "//div[@class='text-center']/a/@href"
            sellername2 = "//div[@class='display-flex-xs align-items-center mb-xs-1']/a[@class='text-link-no-underline text-gray-lightest']/text()"
            sellerurl2 = '//div[@class="display-flex-xs align-items-center mb-xs-1"]/a[@class="text-link-no-underline text-gray-lightest"]/@href'
            comments = '//a[@class="text-link-secondary ml-xs-1 display-flex-xs"]/span/text()'
            location = '//div[@class = "text-center"]/p/text()'
            result = str(response.xpath(name).extract()).replace('[', '').replace(']', '').replace(',', '').replace('\n','') + "," #replace all unncessary characters from loaded in data, makes cleaning easier
            result += str(response.xpath(price).extract_first()).replace('\n','').replace('+','').replace(',', '') + "," 
            result += str(response.xpath(rating).extract()).replace('[', '').replace(']', '').replace("'","") + ","
            result += str(response.xpath(free_shipping).extract_first()).replace('[', '').replace(']', '').replace('\n','') + ","
            result += str(response.xpath(best_seller).extract_first()).replace('[', '').replace(']', '').replace('\n','') + ","
            result += str(response.xpath(sellername).extract_first()).replace('[', '').replace(']', '').replace('\n','') + ","
            result += str(response.xpath(sellername2).extract_first()).replace('[', '').replace(']', '').replace('\n','') + ","
            result += str(response.xpath(sellerurl).extract_first()).replace('[', '').replace(']', '').replace('\n','') + ","
            result += str(response.xpath(sellerurl2).extract_first()).replace('[', '').replace(']', '').replace('\n','') + ","
            result += str(response.xpath(comments).extract_first()).replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace("'","").replace('\n','') + "," 
            result += str(response.xpath(location).extract()).replace('[', '').replace(']', '').replace(',', '').replace("\n","").replace("'","").replace('\n','') + "\n" 
                    
            f.write(result) #write to csv
                