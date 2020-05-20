import pandas as pd
import sqlite3
import datetime
import numpy as np

conn = sqlite3.connect('stock_data.sqlite3')
data = pd.read_sql('select date , 證券代號, 收盤價 from "daily_price" ' , conn , index_col = ['date'])
data.index = pd.to_datetime(data.index , format = '%Y-%m-%d')
end = datetime.date(2018,6,5)
start = datetime.date(2017,1,1)
#start = end + datetime.timedelta(days = -200)
data = data.sort_index() # 最好加這一行，否則可能無法執行data.loc[start : end]
data = data.loc[start : end]
test = data.loc[ datetime.date(2018,1,1) :]

date = list(set(data.index))
company = list(set(data['證券代號']))

#---------------------------第一種寫法---------------------------#
target_data_1 = pd.DataFrame()
for i in range(0,len(date)):
    temp = data.loc[date[i]]
    
    temp_1 = pd.DataFrame(company)
    temp_2 = pd.DataFrame(np.full([len(company) , 1] , np.nan))
    temp_finally = pd.concat([temp_1 , temp_2] , axis = 1)
    temp_finally.columns = ['證券代號' , date[1]]
    temp_finally = temp_finally.set_index('證券代號')
    
    for i in range(0,len(temp)):
        temp_finally.loc[ temp['證券代號'][i] ] = temp['收盤價'][i]
    
    temp_finally = (temp_finally.sort_index()).T
    target_data_1 = pd.concat([target_data_1 , temp_finally] , axis = 0)
#---------------------------第一種寫法---------------------------#


#---------------------------第二種寫法---------------------------#
target_data = pd.DataFrame()
for i in range(0,len(date)):    
    temp_1 = data.loc[date[i]]
    temp_2 = temp_1   
    temp_2 = (temp_2.set_index(['證券代號'])).T
    temp_2['date'] = temp_1.index[0]
    temp_2 = temp_2.set_index(['date'])   
    target_data = pd.concat([target_data , temp_2] , axis = 0)
#---------------------------第二種寫法---------------------------#
 
    
    
    
    
    