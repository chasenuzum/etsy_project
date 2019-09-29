#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 00:13:59 2019

@author: chasenuzum
"""

#Cleaning Data with pandas and numpy
import pandas as pd
import numpy as np


#Load data
rawdatx = pd.read_csv("etsydata.csv")
rawdaty= pd.read_csv("etsysales.csv")

#Filter out un-needed columns; only need these for our analysis/research question
filterx = rawdatx[['sellername2', 'name', 'price', 'comments', 'free_shipping', 'best_seller']]
filtery = rawdaty[['seller', 'sales']]
filtery['sellername'] = filtery['seller']

#Filter out rows where item is 'none'
filterx = filterx[filterx['sellername2'] != 'None']

#Clean x,y values
#strip out extra spaces
filterx['best_seller'] = filterx['best_seller'].str.strip()
filterx['sellername2'] = filterx['sellername2'].str.strip()

#Get rid of none rows where seller name = 'none'
filterx['price'] = filterx['price'].replace(to_replace='None', value='0')
filterx['comments'] = filterx['comments'].replace(to_replace='None', value='0')

#Remove undesirable characters, i.e $, whitespace, commas, text
filterx['price'] = filterx['price'].str.replace('$', '')
filterx['price'] = filterx['price'].replace(r'\s\s\s\s\s\s\s\s\s', '0', regex=True)
filterx['price'] = filterx['price'].str.replace(',', '')
filtery['sales'] = filtery['sales'].str.replace('  on Etsy', '')

#convert continuous string variables to floats
filterx['price'] = filterx['price'].astype('float64') 
filterx['comments'] = filterx['comments'].astype('float64') 
filtery['sales'] = filtery['sales'].astype('float64') 

#Check if y and x are close to match in group
check = filterx['sellername2'].unique() #checked

#Create dummies/quantify qualitative variables
filterx['free_shipping2'] = 0
filterx.loc[(filterx['free_shipping']=="Free shipping to "), 'free_shipping2'] = 1

filterx['bestseller2'] = 0
filterx.loc[(filterx['best_seller']=="Bestseller"), 'bestseller2'] = 1

#Consolidate variables in x to match y
select = filterx[['sellername2', 'price', 'comments', 'free_shipping2', 'bestseller2']] #like a select statement
index_x = select.groupby('sellername2').agg({'price': np.mean, 'comments': np.mean, 'free_shipping2' : np.sum, 'bestseller2' : np.sum}) #group by and aggregate by with SQL like statement
index_y = filtery.set_index('seller') #set index

final_data = pd.merge(index_x, index_y, left_index=True, right_index=True) #merge, like inner join statement in SQL

#Export to CSV
export = final_data.to_csv(r'/Users/chasenuzum/Documents/Spring 2019/Tools of Data Analysis/Etsy Project/EtsyDataClean.csv', index = None, header=True)


