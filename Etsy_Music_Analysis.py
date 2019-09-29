#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 23:19:16 2019

@author: chasenuzum
"""
#Import needed libraries
import patsy as pt
import statsmodels.formula.api as sm
import statsmodels.stats.api as sms
import pandas as pd
import numpy as np

#Load in data
etsy = pd.read_csv("EtsyDataClean.csv")

#Creating dataframe to compare ratings to comments and loading in item data
etsyratings = pd.read_csv("etsydata.csv")
etsyratings = etsyratings[['rating','comments']]
etsyratings['comments'] = etsyratings['comments'].replace(to_replace='None', value='0')
etsyratings['comments'] = etsyratings['comments'].astype('float64') 

#Creating dummy for free-shipping
etsy['free_shipping3'] = 0
etsy.loc[(etsy['free_shipping2']>0), 'free_shipping3'] = 1 #Creating dummy; assumption: free-shipping on one item = free-shipping on all items

#For correlation heatmap
correldat = etsy[["sales","price", "comments", "bestseller2"]]

#summary stats dataset and for ratings
summ = etsy.describe().transpose()
print(summ)
summ.to_csv('etsysummary.csv') #Took screenshot of csv to put in PPT

summratings = etsyratings.describe().transpose() #Checking difference between ratings and comments
print(summratings)
summratings.to_csv('etsyratingsummary.csv') #Took screenshot of csv to put in PPT


y, x = pt.dmatrices("sales ~ price + comments + free_shipping3 + bestseller2", data = etsy) #using this model for analysis
#y2, x2 = pt.dmatrices("sales ~ price + free_shipping2 + bestseller2", data = etsy) #omitted variable bias for all below
#y3, x3 = pt.dmatrices("sales ~ comments + free_shipping2 + bestseller2", data = etsy)
#y4, x4 = pt.dmatrices("sales ~ comments + free_shipping2 + price", data = etsy)


reg = sm.OLS(y,x).fit() #fit model and store table
#reg2 = sm.OLS(y2,x2).fit()
#reg3 = sm.OLS(y3,x3).fit()
#reg4 = sm.OLS(y4,x4).fit()

print(reg.summary()) #print the summary table
#print(reg2.summary())
#print(reg3.summary())
#print(reg4.summary())

#Running test for heteroscedicity
bptest = sms.diagnostic.het_breuschpagan(reg.resid, reg.model.exog) #BP test to check hetero

reg_robust = reg.get_robustcov_results(cov_type='HC0') #White's standard errors
print(reg_robust.summary()) #Run with White's robust SE



import matplotlib.pyplot as plt # Found this on Stackoverflow; works to output ols table as .png in python; can only do one table at a time
#plt.rc('figure', figsize=(12, 7)) #This one is for non-robust model
#plt.text(0.01, 0.05, str(reg.summary()), {'fontsize': 10}, fontproperties = 'monospace')
#plt.axis('off')
#plt.tight_layout()
#plt.savefig('etsyols.png')

plt.rc('figure', figsize=(12, 7)) #This one for robust SE model; same as previous and found on stackoverflow
plt.text(0.01, 0.05, str(reg_robust.summary()), {'fontsize': 10}, fontproperties = 'monospace')
plt.axis('off')
plt.tight_layout()
plt.savefig('etsyolsrobust.png') #Right now it is outputing robust model can change this if needed for non-robust


f = open('etsyols.csv','w')
f.write(reg.summary().as_csv())
f.close() #export OLS table as csv

with open('etsysummary.txt', 'w') as fh:
    fh.write(reg.summary().as_text()) #export OLS table as text

#For correlation Matrix, checking multicollinearity in x's and relationships
import seaborn as sns #seaborn has handy heatmap 

corr = correldat.corr() #get correlation table
etsycorrel = sns.heatmap(corr, #create layout for heatmap
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values,
            annot=True, cmap="Blues") #set up
etsycorrel.autoscale() #fits to screen
fig = etsycorrel.get_figure()
fig.savefig('etsycorrel.png',bbox_inches='tight') #make sure fits to screen

#Scatters to check relationships and data visualization
from plotly import tools
from plotly.offline import plot
import plotly.graph_objs as go

comments = go.Scatter( # initialize scatter object
        x = etsy['comments'], 
        y = etsy['sales'], #enter x,y
        mode = 'markers',
        marker =  {'color': 'red', 
             'size': 6
             }, #set marker details
        name="Sum Item Comments",
        text=etsy['sellername']) #enter text


price = go.Scatter( # initialize scatter object
        x = etsy['price'], 
        y = etsy['sales'], #enter x,y
        mode = 'markers',
        marker =  {'color': 'blue', 
             'size': 6
             }, #set marker details
        name="Average Price",
        text=etsy['sellername']) #enter text 

best_seller = go.Scatter( # initialize scatter object
        x = etsy['bestseller2'], 
        y = etsy['sales'], #enter x,y
        mode = 'markers',
        marker =  {'color': 'green', 
             'size': 6
             }, #set marker details
        name="Best Sellers",
        text=etsy['sellername']) #enter text 

fig2 = tools.make_subplots(rows=3, cols=1) #Create Layout

fig2.append_trace(comments, 1, 1)
fig2.append_trace(price, 2, 1)
fig2.append_trace(best_seller, 3, 1) #Append traces together


fig2['layout'].update(height=600, width=600, title='Etsy Scatters')
plot(fig2) #Plot the scatters


#Compare histogram of comments and ratings; proving ratings are unreliable
import plotly.figure_factory as ff

x = np.log(etsyratings['comments']) #using log so outliers are taken care of for visualization
x = x.replace([-np.inf], 0) #Because some log values go to negative infinity

hist_data = [x] #select Etsy comments
group_labels = ['Etsy Music Comments'] #Set label

dist = ff.create_distplot(hist_data, 
  group_labels, #Using lable above
  bin_size=2,
  show_hist=False,
  show_curve=True, 
  show_rug=True    #Only curve and dash marks
  )
  
plot(dist)

x2 = (etsyratings['rating'])
x2 = x2.dropna() #drop nan values


hist_data2 = [x2] #selecting Etsy ratings
group_labels2 = ['Etsy Ratings'] #Set lable

dist2 = ff.create_distplot(hist_data2, 
  group_labels2, #Using lable above
  bin_size=2,
  show_hist=False,
  show_curve=True, 
  show_rug=True    #Only curve and dash marks
  )
  
plot(dist2)
