#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 18:44:15 2018

@author: ninaad
"""
import pandas as pd
import codecs


f=codecs.open("makemytrip_com-travel_sample.csv",'r',encoding='utf-8',errors='ignore')

fp=open("hotels.csv","w")
for i in f:
    fp.write(i)
fp.close()
f.close()
df=pd.read_csv("hotels.csv", low_memory=False)
latitude=list(df['latitude'])
longitude=list(df['longitude'])
hotelname=list(df['property_name'])
score=list(df['mmt_review_score'])
unique_id=list(df['uniq_id'])
area=list(df['area'])
city=list(df['city'])
city=[str(ijk).lower() for ijk in list(df['city'])]
country=list(df['country'])
hotel_overview=list(df['hotel_overview'])
hotel_star_rating=list(df['hotel_star_rating'])
property_type=list(df['property_type'])
address=list(df['property_address'])
state=list(df['state'])
cities=pd.read_csv("cities.csv",low_memory=False,error_bad_lines=False)
cities_name=list(cities['cities'])
print(len(city),len(latitude),len(longitude),len(hotelname),len(score),len(unique_id),len(area),)
print(len(cities_name))
remove_list=[]
latitude1=[]
longitude1=[]
hotelname1=[]
score1=[]
unique_id1=[]
address1=[]
area1=[]
city1=[]
country1=[]
hotel_overview1=[]
hotel_star_rating1=[]
property_type1=[]
for i in range(len(city)):
    if city[i] not in cities_name:
        print(i)
        remove_list.append(i)
    else:
        property_type1.append(property_type[i])
        address1.append(address[i])
        longitude1.append(longitude[i])
        latitude1.append(latitude[i])
        hotelname1.append(hotelname[i])
        score1.append(score[i])
        unique_id1.append(unique_id[i])
        area1.append(area[i])
        city1.append(city[i])
        country1.append(country[i])
        hotel_overview1.append(hotel_overview[i])
        hotel_star_rating1.append(hotel_star_rating[i])
        
        
df1=pd.DataFrame({'hotel_name':hotelname1})
df2=pd.DataFrame({'type':property_type1})
df3=pd.DataFrame({'city':city1})
df4=pd.DataFrame({'area':area1})
df5=pd.DataFrame({'country':country1})
df6=pd.DataFrame({'address':address1})
df7=pd.DataFrame({'latitude':latitude1})
df8=pd.DataFrame({'longitude':longitude1})
df9=pd.DataFrame({'unique_id':unique_id1})
df10=pd.DataFrame({'hotel_overview':hotel_overview1})
df11=pd.DataFrame({'hotel_star_rating':hotel_star_rating1})
df12=pd.DataFrame({'review rating':score1})
df13=pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12],axis=1)
df13.to_csv('hoteldatabase.csv',index=False)