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

#reading the data on export from 2001-2021
export=pd.read_csv('FAOSTAT_data_en_export_01_21.csv',dtype={'Year':str})

#renaming columns to appropriate names
export=export.rename(columns={'Area':'Country','Value':'Total_Export'})

#listing the necessary variables
export_vars=['Domain','Country','Item','Year','Unit','Total_Export']

#seleting vars
export=export[export_vars]

#export in millions of tonnes
export['Total_Export']=export['Total_Export']/1e6
export['Total_Export']=export['Total_Export'].round(5)

#grouping the data by year and country
export_gr=export.groupby(['Country','Year']).sum()

#renaming the name of Moldova
export_gr=export_gr.rename({'Republic of Moldova':'Moldova'})
export_gr=export_gr.reset_index()

#bulding linegraphs of export for each country between 2001-2021
sns.set_style("whitegrid")
plt.figure(figsize=(12,8))
sns.lineplot(data=export_gr, x='Year', y='Total_Export', hue='Country', linewidth=2.5)
plt.title('Export by Country and Year', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Export (Millions of Tonnes)', fontsize=14)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('total_export.png',dpi=300,bbox_inches='tight')

#%%
#filtering out the data on wheat export
wheat_export=export.query("Item=='Wheat'")

#wheat export in millions of tonnes
wheat_export=wheat_export.rename(columns={'Total_Export':'Wheat_Export'})

#grouping the data by year and country
wheat_export_gr=wheat_export.groupby(['Country','Year']).sum()

#renaming the name of Moldova
wheat_export_gr=wheat_export_gr.rename({'Republic of Moldova':'Moldova'})
wheat_export_gr=wheat_export_gr.reset_index()

#bulding linegraphs
sns.set_style("whitegrid")
plt.figure(figsize=(12,8))
sns.lineplot(data=wheat_export_gr, x='Year', y='Wheat_Export', hue='Country', linewidth=2.5)
plt.title('Wheat Export by Country and Year', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Wheat Export (Millions of Tonnes)', fontsize=14)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('wheat_export.png',dpi=300,bbox_inches='tight')

#%%
#reading a csv file on total data on production
total_data=pd.read_csv('total_data_eeca.csv',dtype={'Year':str})

#joining export data onto total data
total_data=total_data.merge(export_gr,on=['Country','Year'],how='left',validate='1:1',indicator=True)
print(total_data['_merge'].value_counts())
total_data=total_data.drop(columns='_merge')

total_data=total_data.merge(wheat_export_gr,on=['Country','Year'],how='left',validate='1:1',indicator=True)
print(total_data['_merge'].value_counts())
total_data=total_data.drop(columns='_merge')

#renaming the prc_wheat column and saving the results
total_data=total_data.rename(columns={'prc_wheat':'Percent_Wheat_Prod'})
total_data.to_csv('total_data_EECA.csv',index=False)
