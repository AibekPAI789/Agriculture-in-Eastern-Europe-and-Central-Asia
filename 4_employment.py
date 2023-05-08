#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 08:49:31 2023

@author: aibekkabyldin
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#reading the all countries data on employment
raw_empl=pd.read_csv('API_SL.AGR.EMPL.ZS_DS2_employment.csv')

#EECA countries list
country_list=['Bulgaria','Belarus','Czechia','Hungary','Kazakhstan','Kyrgyzstan','Poland','Moldova','Romania','Russian Federation','Slovakia','Tajikistan','Turkmenistan','Ukraine','Uzbekistan']

#selecting EECA countries
raw_empl_eeca = raw_empl.loc[raw_empl['Country Name'].isin(country_list)]

#editing raw data 
raw_empl_eeca['Indicator Name'] = raw_empl_eeca['Indicator Name'].replace({'Employment in agriculture (% of total employment) (modeled ILO estimate)': 'Employment in agriculture (%)'})

#selected years
years=['2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021']

#cleaning data until it is appropriate
raw_empl_eeca=raw_empl_eeca.set_index(['Country Name','Indicator Name'])
raw_empl_eeca=raw_empl_eeca[years]

#dropping years with missing data
raw_empl_eeca=raw_empl_eeca.drop(columns={'2020','2021'})

#setting only Country Name as the index
empl_data_01_19=raw_empl_eeca.reset_index(level=1) 

#saving the employment data in agriculture for 2001-2019
empl_data_01_19.to_csv('employment_data.csv')

#%%
#reading the total data in 2001-2021
total_data_EECA=pd.read_csv('total_data_EECA.csv',dtype={'Year':str})

#selecting up necessary variables from total data for further correlation analysis
total_data_for_corr=total_data_EECA[['Country','Year','Total_Prod']]

#%%
#cleaning up employment data 
empl_data_01_19_gr=empl_data_01_19.drop(columns='Indicator Name')
empl_data_01_19_gr=empl_data_01_19_gr.reset_index()

#restructuring employment data
empl_data_melted=empl_data_01_19_gr.melt(id_vars='Country Name',var_name='Year',value_name='Employment Rate')
empl_data_melted=empl_data_melted.rename(columns={'Country Name':'Country'})

#plotting employment rates
sns.set_style("whitegrid")
plt.figure(figsize=(12,8))
sns.lineplot(data=empl_data_melted, x='Year', y='Employment Rate', hue='Country', linewidth=2.5)
plt.title('Agriculture Employment Rate by Country and Year', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Employment Rate (%)', fontsize=14)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('employment_rates.png',dpi=300,bbox_inches='tight')

#%%
#merging two data with right join so that 2020-2021 data on production 
#is not be counted because employment data is until 2019
merged_for_corr=total_data_for_corr.merge(empl_data_melted, on=['Country', 'Year'],how='right',indicator=True)
print(merged_for_corr['_merge'].value_counts())
merged_for_corr=merged_for_corr.drop(columns='_merge')

# grouping the data for correlation by country
corr_grouped_data = merged_for_corr.groupby('Country')

# calculating the correlation coefficients between agriculture production 
#and employment rate for each country
correlations = corr_grouped_data.apply(lambda x: x['Employment Rate'].corr(x['Total_Prod']))

# displaying the correlations for each country
print('\nCorrelation coefficients:\n')
print(correlations)

#scatter plots with linear regression line and saving them
for country, data in corr_grouped_data:
    sns.regplot(x='Employment Rate', y='Total_Prod', data=data)
    plt.xlabel('Employment Rate in Agriculture(%)')
    plt.ylabel('Agriculture Production (mln tonnes)')
    plt.title(f'Scatter Plot of Employment Rate and Agroculture Production for {country}')
    plt.savefig(f'corr_analysis_for_{country}')
    plt.clf()
