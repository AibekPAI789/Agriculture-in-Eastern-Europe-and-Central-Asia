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

#reading the total data from previous script
total_data=pd.read_csv('total_data_eeca.csv',dtype={'Year':str})

#selecting total data only for 2021 year in millions of tonnes
data_2021=total_data.query("Year=='2021'")
data_2021=data_2021.set_index('Country')

#reading the data on detailed production 2001-2021
data_prod=pd.read_csv('FAOSTAT_data_en_production_01_21.csv',dtype={'Year':str})

#renaming columns: Area to Country and Value to Total_Prod
data_prod=data_prod.rename(columns={'Area':'Country','Value':'Total_Prod'})

#listing the necessary variables
variables=['Domain','Country','Item','Year','Unit','Total_Prod']

#selecting up the data by necessary variables
prod=data_prod[variables]

#select detailed production data for 2021
prod_2021=prod.query("Year=='2021'")

#converting values to millions of tonnes
prod_2021['Total_Prod']=prod_2021['Total_Prod']/1e6

# Grouping the data by country and product, and sum the production quantities
data_2021_gr = prod_2021.groupby(['Country', 'Item']).sum()

# Find the most produced product for each country in mln tonnes
data_2021_most_prod=data_2021_gr.groupby('Country').apply(lambda x: x.nlargest(1, 'Total_Prod'))
data_2021_most_prod.reset_index(level=0, inplace=True) 
data_2021_most_prod.reset_index(level=1, inplace=True) 
data_2021_most_prod=data_2021_most_prod.drop(columns='Country')
data_2021_most_prod=data_2021_most_prod.rename(columns={'Total_Prod':'Value'})

#renaming the name of Moldova
data_2021_most_prod=data_2021_most_prod.rename({'Republic of Moldova':'Moldova'})

#printing the results
print('\nThe most produced product of each country and its value in mln tons:\n')
print(data_2021_most_prod)
    
#percentage of the most produced item in the total production
data_2021_most_prod['prct_in_total']=100*data_2021_most_prod['Value']/data_2021['Total_Prod']
data_2021_most_prod[['Value','prct_in_total']]=data_2021_most_prod[['Value','prct_in_total']].round(2)

#adding a column for units of values
data_2021_most_prod.insert(loc=2,column='Unit of Values',value='mln tonnes')

#selecting the data by Item and its share in total production
data_2021_shares=data_2021_most_prod[['prct_in_total','Item']]
data_2021_shares=data_2021_shares.reset_index()
data_2021_shares=data_2021_shares.set_index(['Country','Item'])

#plotting the histogram
fig,ax=plt.subplots()
data_2021_shares.plot.bar(ax=ax,figsize=(10,6))
ax.set_xlabel('Country and the Most Produced Product')
ax.set_ylabel('Percentage')
ax.set_title('Percentage of the Most Produced Product in Total Production by Country')
fig.tight_layout()
fig.savefig('prct_prod_most.png')

#%%
#reset the index to numeric index
data_2021_most_prod=data_2021_most_prod.reset_index()

#grouping the data by Product and Country
data_2021_most_prod_gr = data_2021_most_prod.groupby(['Item','Country']).sum()

#grouping then by Product
data_2021_by_product = data_2021_most_prod_gr.groupby('Item')

#reporting countries for each product
for product, group in data_2021_by_product:
    print(f"Countries with the most produced {product}:")
    print(group['Value'])  
    print()
    
#%%
#reading the data on agriculture export for 2001-2021
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

#selecting export data for 2021
export_2021=export.query("Year=='2021'")

# Grouping the data by country and product, and sum the production quantities
export_2021_gr = export_2021.groupby(['Country', 'Item']).sum()

# Find the most produced product for each country in mln tonnes
export_2021_most_prod=export_2021_gr.groupby('Country').apply(lambda x: x.nlargest(1, 'Total_Export'))
export_2021_most_prod.reset_index(level=0, inplace=True) 
export_2021_most_prod.reset_index(level=1, inplace=True) 
export_2021_most_prod=export_2021_most_prod.drop(columns='Country')
export_2021_most_prod=export_2021_most_prod.rename(columns={'Total_Export':'Value'})

#renaming the name of Moldova
export_2021_most_prod=export_2021_most_prod.rename({'Republic of Moldova':'Moldova'})

#printing the results
print('\nThe most exported product by country and its value in mln ton:')
print(export_2021_most_prod)
    
#percentage of the most exported item in the total export
export_2021_most_prod['prct_in_total']=100*export_2021_most_prod['Value']/data_2021['Total_Export']
export_2021_most_prod[['Value','prct_in_total']]=export_2021_most_prod[['Value','prct_in_total']].round(2)

#adding a column for units of values
export_2021_most_prod.insert(loc=2,column='Unit of Values',value='mln tonnes')

#selecting the data by product and its share in total production
export_2021_shares=export_2021_most_prod[['prct_in_total','Item']]
export_2021_shares=export_2021_shares.reset_index()
export_2021_shares=export_2021_shares.set_index(['Country','Item'])

#plotting the histogram
fig,ax1=plt.subplots()
export_2021_shares.plot.bar(ax=ax1,figsize=(10,6))
ax1.set_xlabel('Country and the Most Exported Product')
ax1.set_ylabel('Percentage')
ax1.set_title('Percentage of the Most Exported Product in Total Export by Country')
fig.tight_layout()
fig.savefig('prct_export_most.png')

#%%
#reset the index to numeric index
export_2021_most_prod=export_2021_most_prod.reset_index()

#grouping the data by Product and Country
export_2021_most_prod_gr = export_2021_most_prod.groupby(['Item','Country']).sum()

#grouping then by Product
export_2021_by_product = export_2021_most_prod_gr.groupby('Item')

#reporting countries for each product in mln tons
for product, group in export_2021_by_product:
    print(f"Countries with the most exported {product}:")
    print(group['Value'])  
    print()

#%%
#merging the data on the most produced and exported products by country in 2021
merged_2021_most=data_2021_most_prod.merge(export_2021_most_prod,on='Country',how='left',validate='1:1',indicator=True)
print(merged_2021_most['_merge'].value_counts())
merged_2021_most=merged_2021_most.drop(columns='_merge')

#renaming columns in the merged data on the most products
colnames={'Item_x':'produced_item','Value_x':'produced_value','Unit of Values_x':'product_units','prct_in_total_x':'prct_in_total_prod','Item_y':'exported_item','Value_y':'exported_value','Unit of Values_y':'export_units','prct_in_total_y':'prct_in_total_export'}
merged_2021_most=merged_2021_most.rename(columns=colnames)

#saving the most 2021 data to a csv file
merged_2021_most.to_csv('the_most_data_2021.csv',index=False)
