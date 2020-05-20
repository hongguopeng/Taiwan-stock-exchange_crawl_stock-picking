import pandas as pd
import sqlite3
import datetime
import numpy as np

conn = sqlite3.connect('stock_data.sqlite3')
data = pd.read_sql('select date , 證券代號, 當月營收 from "monthly_report" ' , conn , index_col = ['date'])
data.index = pd.to_datetime(data.index , format = '%Y-%m-%d')
select_date = datetime.datetime(2017,3,16)
year , month , day = select_date.year , select_date.month , select_date.day

if day < 10:
      target_year = year
      target_month = month - 1
      target_day = 10
elif day >= 10:
      target_year = year
      target_month = month
      target_day = 10 
      
#target_date = datetime.datetime(target_year , target_month , target_day) 

target_date_list = [str(target_year) + '-' + str(target_month) + '-' + str(target_day)] 
for i in range(0,10):
      if target_month == 1:
            target_month = 12
            target_year = target_year - 1
      elif target_month != 1:
            target_month = target_month - 1
      target_date_list.append(str(target_year) + '-' + str(target_month) + '-' + str(target_day))      
            
            
target_date = pd.to_datetime(target_date_list)      
data = data.loc[target_date]   


date = list(set(data.index))
company = list(set(data['證券代號'])) 
target_data = pd.DataFrame()
for i in range(0,len(date)):
#for i in range(0,1):      
    temp_1 = data.loc[date[i]]
    temp_2 = temp_1   
    temp_2 = (temp_2.set_index(['證券代號'])).T
    temp_2['date'] = temp_1.index[0]
    temp_2 = temp_2.set_index(['date'])   
    target_data = pd.concat([target_data , temp_2] , axis = 0)
      


