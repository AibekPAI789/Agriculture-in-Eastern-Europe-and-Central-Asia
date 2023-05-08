#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 13:48:06 2023

@author: aibekkabyldin
"""

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

plt.rcParams['figure.dpi'] = 300

#reading and setting polygon for Czechia
CZE=gpd.read_file('SHAPEFILES/zipped/CZE_data.zip')
CZE=CZE[['NAME_ENGLI','geometry']]
CZE=CZE.rename(columns={'NAME_ENGLI':'country'})
CZE['country'] = CZE['country'].replace({'Czech Republic':'Czechia'})

#reading and setting polygon for Hungary
HUN=gpd.read_file('SHAPEFILES/zipped/hun_admbnda_osm_20220720_shp.zip')
HUN=HUN[['ADM0_EN','geometry']]
HUN=HUN.rename(columns={'ADM0_EN':'country'})

#reading and setting polygon for Bulgaria
BGR=gpd.read_file('SHAPEFILES/zipped/BGR_data.zip')
BGR=BGR[['NAME_ENGLI','geometry']]
BGR=BGR.rename(columns={'NAME_ENGLI':'country'})

#reading and setting polygon for Belarus
BLR=gpd.read_file('SHAPEFILES/zipped/BLR_data.zip')
BLR=BLR[['NAME_ENGLI','geometry']]
BLR=BLR.rename(columns={'NAME_ENGLI':'country'})

#reading and setting polygon for Kazakhstan
KAZ=gpd.read_file('SHAPEFILES/zipped/KAZ_data.zip')
KAZ=KAZ[['NAME_ENGLI','geometry']]
KAZ=KAZ.rename(columns={'NAME_ENGLI':'country'})

#reading and setting polygon for Kyrgyzstan
KGZ=gpd.read_file('SHAPEFILES/zipped/kgz-administrative-divisions-shapefiles.zip')
KGZ=KGZ[['ADM0_EN','geometry']]
KGZ=KGZ.rename(columns={'ADM0_EN':'country'})

#reading and setting polygon for Moldova
MDA=gpd.read_file('SHAPEFILES/zipped/MDA_data.zip')
MDA=MDA[['NAME_ENGLI','geometry']]
MDA=MDA.rename(columns={'NAME_ENGLI':'country'})

#reading and setting polygon for Poland
POL=gpd.read_file('SHAPEFILES/zipped/POL_data.zip')
POL=POL[['NAME_ENGLI','geometry']]
POL=POL.rename(columns={'NAME_ENGLI':'country'})

#reading and setting polygon for Romania
ROU=gpd.read_file('SHAPEFILES/zipped/ROU_data.zip')
ROU=ROU[['NAME_ENGLI','geometry']]
ROU=ROU.rename(columns={'NAME_ENGLI':'country'})

#reading and setting polygon for Russia
RUS=gpd.read_file('SHAPEFILES/zipped/RUS_data-5.zip')
RUS=RUS[['NAME_ENGLI','geometry']]
RUS=RUS.rename(columns={'NAME_ENGLI':'country'})
RUS['country'] = RUS['country'].replace({'Russia':'Russian Federation'})

#reading and setting polygon for Slovakia
SVK=gpd.read_file('SHAPEFILES/zipped/svk_admbndp_geoportalsk_itos_20220707_shp.zip')
SVK=SVK[['ADM0_EN','geometry']]
SVK=SVK.rename(columns={'ADM0_EN':'country'})

#reading and setting polygon for Tajikistan
TJK=gpd.read_file('SHAPEFILES/zipped/TJK_data-3.zip')
TJK=TJK[['NAME_ENGLI','geometry']]
TJK=TJK.rename(columns={'NAME_ENGLI':'country'})

#reading and setting polygon for Turkmenistan
TKM=gpd.read_file('SHAPEFILES/zipped/TKM_data-2.zip')
TKM=TKM[['NAME_ENGLI','geometry']]
TKM=TKM.rename(columns={'NAME_ENGLI':'country'})

#reading and setting polygon for Ukraine
UKR=gpd.read_file('SHAPEFILES/zipped/UKR_data.zip')
UKR=UKR[['NAME_ENGLI','geometry']]
UKR=UKR.rename(columns={'NAME_ENGLI':'country'})

#reading and setting polygon for Uzbekistan
UZB=gpd.read_file('SHAPEFILES/zipped/UZB_data-4.zip')
UZB=UZB[['NAME_ENGLI','geometry']]
UZB=UZB.rename(columns={'NAME_ENGLI':'country'})

#JOINING ALL MAPS TO ONE
REGION = pd.concat([BGR,BLR,CZE,HUN,KAZ,KGZ,MDA,POL,ROU,RUS,SVK,TJK,TKM,UKR,UZB], axis=0, ignore_index=True)

#saving the shp file for the region
REGION.to_file('REGION.shp')
