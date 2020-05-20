import pandas as pd
import sqlite3
import datetime

conn = sqlite3.connect('stock_data.sqlite3')
data = pd.read_sql('select date , 證券代號, 股本合計 from "balance_sheet" ' , conn , index_col = ['date'])
# data是以公司代號的先後排序
data.index = pd.to_datetime(data.index , format = '%Y-%m-%d')
select_date = datetime.date(2017 , 5 , 10)

#---------------------------第一種寫法(次要寫法)---------------------------#
#date_m_d = [[5  , 8  , 11  ,3] , 
#            [15 , 14 , 14 , 31]]
#date_list = []
#for i in range(0 , len(date_m_d[0])):
#    date_list.append(datetime.date(select_date.year , 
#                                   date_m_d[0][i] , 
#                                   date_m_d[1][i]))
#
#date_delta = []
#for j in range(0 , len(date_list)):
#    temp = (select_date - date_list[j]).days
#    date_delta.append(temp)    
#date_delta = pd.DataFrame(date_delta)  
#  
#mini = (date_delta.loc[date_delta.iloc[:,0] >= 0]).min()    
#for j in range(0 , len(date_list)):
#    if date_delta.iloc[j , 0] == mini[0]:
#        target_date = date_list[j]       
#
#target_date = datetime.datetime(target_date.year , target_date.month , target_date.day)        
#target_data_1 = data.loc[target_date]
#---------------------------第一種寫法---------------------------#


#---------------------------第二種寫法(主要寫法)---------------------------#
data = data.sort_index() # 將data以日期的先後排序
target_data = data.loc[:select_date] # 想要這樣寫(偷懶)，必須先寫data = data.sort_index()
target_data = target_data.loc[target_data.index[-1]]

target_data_temp = target_data
target_data_temp = target_data_temp.set_index(['證券代號']).T
target_data_temp['date'] = target_data.index[0]
target_data = target_data_temp.set_index(['date'])
#---------------------------第二種寫法---------------------------#







