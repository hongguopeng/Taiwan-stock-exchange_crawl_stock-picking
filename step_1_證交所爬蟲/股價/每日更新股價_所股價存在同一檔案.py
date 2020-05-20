import datetime
import requests
import json
import pandas as pd
import numpy as np
import os
import sqlite3
import time

#if not os.path.isdir('每日股價資料夾'):
#	os.mkdir('每日股價資料夾')	

start = ['2018', '06' , '12']
end = ['2018' , '07' , '15']
start_date = datetime.date(int(start[0]), int(start[1]), int(start[2]))
end_date = datetime.date(int(end[0]), int(end[1]), int(end[2]))
today = datetime.date.today()
delta_start = today - start_date
delta_end = today - end_date

#end = [str(today.year) , str(today.month) , str(today.day)]

if delta_start.days > 0 and delta_end.days >= 0:
      during_day = str(datetime.date(int(end[0]), int(end[1]), int(end[2])) - datetime.date(int(start[0]), int(start[1]), int(start[2])))
      during_day = int(during_day.split(' ')[0]) + 1
      
      date = pd.DataFrame(pd.date_range( start[0] + start[1] +  start[2], periods = during_day))
      date = date.astype(str)
      date = date.apply(lambda s : s.str.replace('-', ''))
      
      data_all = pd.DataFrame()     
      for day in range(len(date)):
          url = 'http://www.tse.com.tw/exchangeReport/MI_INDEX?response=json&date=' + date.iloc[day,0] + '&type=ALLBUT0999&_=1527931290611'
          headers = {'user-agent' : 'Mozilla/5.0(iPhone; CPU iPhone OS 7_1_2 like Mac OS X) App leWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53'}
          response = requests.get(url , headers = headers)
          data_temp = json.loads(response.text)
          
          if data_temp['stat'] == 'OK':
              print('Weekday' + date.iloc[day,0] + ': Earn Money~')
              
              data_list = data_temp['data9']
              item = data_temp['fields9']
              
              data = pd.DataFrame()
              data_list = np.array(data_list) 
              data = pd.DataFrame(data_list)
              data.columns = item  
              data = data.astype(str)
              data = data.apply(lambda s : s.str.replace(',', ''))
              data['date'] = list(date.iloc[day])[0]
              data = data.set_index(['date' , '證券代號'])
              data = data.apply(lambda s : pd.to_numeric(s, errors='coerce'))
              data = data[data.columns[data.isnull().sum(axis = 0) != data.shape[0]]]
              data_all = pd.concat([data_all , data] , axis = 0)
          #    data = data.loc[ data['收盤價'].notnull() ] 
              
          elif data_temp['stat'] == '很抱歉，沒有符合條件的資料!':
              print('Weekend' + date.iloc[day,0] + ': boo~ boo~')
              
          time.sleep(10)    
          
      conn = sqlite3.connect('stock_data.sqlite3') 
      daily_price = 'daily_price'   
      data_all.to_sql(daily_price , conn , if_exists = 'append')    
          
#      path = os.path.join('每日股價資料夾' , 'daily_price' + '.csv' )  
#      data_all.to_csv(path, encoding = 'utf_8_sig')
      
      
 
##-------------------讀取剛才存的sqlite3與csv-------------------#      
#f = open(path , encoding = 'utf_8_sig') # 在讀csv時傳入的參數不是文件名而是文件的路徑，就會報這個错。不能直接用pd.read_csv去讀檔案例如: data_read = pd.read_csv(path , index_col = ['證券代號'])
#data_read = pd.read_csv(f, index_col = ['證券代號'] )
#
##data_sql = pd.read_sql('select * from "daily_price" where 證券代號 = "0050"', conn)
#data_0050 = pd.read_sql('select date , 證券代號 , 開盤價 , 收盤價 , 最高價 , 最低價 , 成交股數 from "daily_price" where 證券代號 = "0050"' , conn , index_col = ['date'])
#data_0050.index = pd.to_datetime(data_0050.index , format = '%Y%m%d')
#data_0050.rename(columns = {'證券代號':'stock_id' , '收盤價':'close', '開盤價':'open', '最高價':'high', '最低價':'low', '成交股數':'volume'}, inplace=True)
#
#import matplotlib.pyplot as plt
#plt.rcParams["figure.figsize"] = (20,10)
#data_0050['close'].plot()      
#from talib import abstract
#test = abstract.RSI(data_0050)
##-------------------讀取剛才存的sqlite3與csv-------------------# 