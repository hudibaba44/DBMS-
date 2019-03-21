#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 05:38:33 2018

@author: ninaad
"""

import pandas as pd
df=pd.read_csv('hoteldatabase.csv')
value=len(df['city'])
room_id=[i for i in range(1,value*30+1)]
room_type=['single','double','king','queen','studio']
ac=['AC', 'NON-AC']
unique_id=list(df['unique_id'])
rooms=[]
room_ac=[]
m=0
count=0
n=0
dictionary={}
idofhotels=[]
list_of_rooms=[]
for i in unique_id:
    list_of_rooms=[]
    for room_value in range(30):
        list_of_rooms.append((room_type[room_value%5],ac[n]))
        n=(n+1)%2
    list_of_rooms.sort()
    for values in list_of_rooms:
        rooms.append(values[0])
        room_ac.append(values[1])
        idofhotels.append(i)
df1=pd.DataFrame({'room_id':room_id})
df2=pd.DataFrame({'hotel_id':idofhotels})
df3=pd.DataFrame({'room_type':rooms})        
df4=pd.DataFrame({'ac/non-ac':room_ac})
df5=pd.concat([df1,df2,df3,df4],axis=1)
df5.to_csv('room_database.csv',index=False)
        
            
            
    