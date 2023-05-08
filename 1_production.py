#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 08:53:22 2023

@author: aibekkabyldin
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#setting parameters
plt.rcParams['figure.dpi']=300
sns.set_theme(style='white')

#reading the data on agriculture production 
data_prod=pd.read_csv('FAOSTAT_data_en_production_01_21.csv',dtype={'Year':str})

#renaming columns: Area to Country and Value to Total_Prod
data_prod=data_prod.rename(columns={'Area':'Country','Value':'Total_Prod'})

#listing the necessary variables
variables=['Domain','Country','Item','Year','Unit','Total_Prod']

#selecting up the data by necessary variables
prod=data_prod[variables]

#grouping the data by countries and years
region=prod.groupby(['Country','Year']).sum()

#renaming 'Republic of Moldova' to just Moldova for further convenience on plotting
region=region.rename({'Republic of Moldova':'Moldova'})

#converting the data to millions of tonnes
region['Total_Prod']=region['Total_Prod']/1e6

#setting the regular numeric index
region=region.reset_index()

#reshaping the data so that each row represents a country and each column represents a year
region_pivot = region.pivot(index='Country', columns='Year', values='Total_Prod')

#selecting last 10 years from the data
years=['2012','2013','2014','2015','2016','2017','2018','2019','2020','2021']
last_10_years=region_pivot[years]

#building a heatmap of agriculture production by country and year
sns.heatmap(last_10_years, cmap='Paired')
plt.title('Agriculture Production (millions of tonnes)')
plt.savefig('agriculture_production.png', dpi=300, bbox_inches='tight')

#%%
#filtering out the data on wheat production
wheat_prod=prod.query("Item=='Wheat'")

#cleaning up wheat production data 
wheat_vars=['Country','Item','Year','Total_Prod','Unit']
wheat_prod=wheat_prod[wheat_vars]

#wheat production in millions of tonnes
wheat_prod['Total_Prod']=wheat_prod['Total_Prod']/1e6

#renaming column Total_Prod to Wheat_Prod
wheat_prod=wheat_prod.rename(columns={'Total_Prod':'Wheat_Prod'})

#grouping the data by year and country
wheat_gr=wheat_prod.groupby(['Country','Year']).sum()

#renaming the name of Moldova
wheat_gr=wheat_gr.rename({'Republic of Moldova':'Moldova'})

#setting the numreic index
wheat_gr=wheat_gr.reset_index()

#reshaping the data so that each row represents a country and each column represents a year
wheat_pivot = wheat_gr.pivot(index='Country', columns='Year', values='Wheat_Prod')

#last 10 years of wheat production for heatmap
last_10_years_wheat=wheat_pivot[years]

#building a heatmap 
sns.heatmap(last_10_years_wheat, cmap='Paired')
plt.title('Wheat Production (millions of tonnes)')
plt.savefig('wheat_production.png', dpi=300, bbox_inches='tight')

#%%
#merging the data on total production and wheat production
total_data=region.merge(wheat_gr,on=['Country','Year'],how='left',validate='1:1',indicator=True)
print(total_data['_merge'].value_counts())
total_data=total_data.drop(columns='_merge')

#percentage of wheat production in total agriculture production
total_data['prc_wheat']=100*total_data['Wheat_Prod']/total_data['Total_Prod']

#saving the results to a csv file
total_data.to_csv('total_data_eeca.csv',index=False)
