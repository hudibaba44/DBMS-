#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 19:41:39 2018

@author: ninaad
"""

f=open('/home/ninaad/Downloads/stationcode.txt','r')

a=f.read()
b=a.split('\n')
fw=open('/home/ninaad/Downloads/stationcodenew.csv','w')
fw.write('Station Name,Station code\n')
for i in b:
    j=i.split(' ')
    code=j[-1]
    station=j[:-1]
    station=' '.join(station)
    fw.write(station)
    fw.write(',')
    fw.write(code)
    fw.write('\n')
fw.close()
f.close()
    
    