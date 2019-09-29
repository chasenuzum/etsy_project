#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 18:28:02 2019

@author: chasenuzum
"""
#RUN THIS SCRAPE SECOND WITH UNIQUE SELLER URLS
#Cleaning data with pandas
import pandas as pd
import numpy as np
import scrapy


prodata = pd.read_csv("/Users/chasenuzum/Documents/Spring 2019/Tools of Data Analysis/etsydata.csv") #load in etsy item data 

unique_sellerurls = prodata[[' sellerurl2', ' sellername2']] #select statement

#Get urls of sellers for next scrapy
sellers = unique_sellerurls.drop_duplicates(subset=' sellername2') #drops duplicate URLs
sellers = sellers.replace(to_replace='None', value=np.nan).dropna() #drops 'None' value rows
sellersurl = sellers[' sellerurl2'].tolist() #moves to a list for scrapy to take


filename = 'etsysales.csv' 

class EtsySpider2(scrapy.Spider):
    name = "etsy_spider2"
    DOWNLOAD_DELAY = 0 #No delay
    DOWNLOAD_TIMEOUT = 250 #Set timeout for a little bit longer since longer list of starts
    start_urls = sellersurl #SET START URL AS LIST DEFINED PREVIOUSLY
    with open(filename, 'w') as f:
        f.write('seller,sales,location\n') #Make no spaces between column names


    def parse(self, response): #Simpler scarpe than before, no next page or items to parse through
        with open(filename, 'a') as f:
            seller = "//h1[@class='mb-xs-1']/text()" #Find xpaths
            sales = "//div/p/span[@class='shop-sales hide-border no-wrap']/text()|//div/p/span[last()]/a/text()"
            location = "//div/p/span[@class='shop-location']/text()"

            result = str(response.xpath(seller).extract_first()) + "," #Prelimiary data cleaning
            result += str(response.xpath(sales).extract_first()).replace('Sales','').replace('Sale','') + "," 
            result += str(response.xpath(location).extract_first()).replace(',','') + "\n"

                    
            f.write(result) #write to csv
                