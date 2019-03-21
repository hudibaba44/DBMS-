#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 06:04:23 2018

@author: ninaad
"""

import pandas as pd 
df=pd.read_csv('/home/ninaad/Downloads/Train_details_22122017.csv')
station_code=[i.lower() for i in df['Station Code']]
station_name=[i.lower() for i in df['Station Name']]
station_name=list(set(station_name))
station_name.sort()
city_name=[]
for name in station_name:
    print(name)
    partial=name.split(' ')
    print(partial)
    if(len(partial[-1])<5):
        partial.remove(partial[-1])
    partial=' '.join(partial)
    print(partial)
    ind=station_name.index(name)
    city_name.append(partial)

print(len(set(station_code)),len(set(station_name)))
print(len(set(city_name)))
city_name=list(set(city_name))
f=open('cities.csv','w')
f.write('cities')
for i in city_name:
    f.write(i)
    f.write('\n')
f.close()