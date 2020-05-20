import requests
import pandas as pd
import numpy as np
import time
import datetime
import sqlite3
import os
import random
from requests.exceptions import ConnectionError
from io import StringIO

txt_list = ['bs_item.txt' , 'fs_item.txt' , 'cf_item.txt']
table_list = [[] , [] , []]  # table_list = [資產負債表 , 綜合損益表 , 現金流量表]
for read in range(0 , 3):
    path = os.path.join(txt_list[read])
    txt_open = open(path, 'r')
    for i in txt_open:
        table_list[read].append(i.replace('\n' , ''))
    
start_year = 2017
end_year = 2017
now = datetime.datetime.now()

balance_sheet , financial_statements , cash_flow = pd.DataFrame() , pd.DataFrame() , pd.DataFrame()
for year in range(start_year , end_year + 1):
      
    company = pd.DataFrame()
    for month in range(1 , 13):
        if year == now.year and month == now.month:
            break
        else:
          url_company = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_' + str(year - 1911) + '_' + str(month) + '_0.html'
          headers = {'user-agent' : 'Mozilla/5.0(iPhone; CPU iPhone OS 7_1_2 like Mac OS X) App leWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53'}
          try: 
              r = requests.get(url_company , headers = headers)     
              r.encoding = 'big5'
          except ConnectionError:
              stop_time = 150
              print('證交所拒絕連線,暫停' + str(stop_time) + '秒')
              time.sleep(stop_time)    
              r = requests.get(url_company , headers = headers)     
              r.encoding = 'big5'      
          
          dfs = pd.read_html(StringIO(r.text))
      
          company_unit = dfs[0]
          company_unit = company_unit.iloc[:,0]
        
          company_unit = company_unit.apply(lambda s : pd.to_numeric(s , errors = 'coerce'))
          company_unit = company_unit.loc[company_unit.notnull()]
          company_unit = company_unit.apply(lambda s : str(s))
          company_unit = company_unit.apply(lambda s : s.replace('.0', ''))
          company_unit = pd.DataFrame(sorted(list(company_unit)))
          company = pd.concat([company , company_unit] , axis = 0)
          time.sleep(2)
          
    company = list(np.array(company).tolist())
    company = [i[0] for i in company]
    company = sorted(list(set(company)))
    
    for com in range(0 , len(company)):
        temp_season = [pd.DataFrame() , pd.DataFrame() , pd.DataFrame()]   # temp_season = [資產負債表 , 綜合損益表 , 現金流量表]
        for season in range(1 , 5):
                  
              url = 'https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID='\
                      + str(company[com]) + '&SYEAR=' + str(year - 1911) +\
                      '&SSEASON=' + str(season) + '&REPORT_ID=C'
              
              try:
                  res = requests.get(url , headers = headers)
                  res.encoding = 'big5'
                  time.sleep(8 + random.uniform(0 , 1)) 
              except ConnectionError:
                  stop_time = 150
                  print('證交所拒絕連線,暫停' + str(stop_time) + '秒')
                  time.sleep(stop_time)    
                  res = requests.get(url , headers = headers)
                  res.encoding = 'big5'
                  time.sleep(8 + random.uniform(0 , 1))
            
              try:
                  temp_unit = pd.read_html(StringIO(res.text))
              except ValueError:
                  stop_time = 150
                  print('No Tables Found!!' + '-' +  str(stop_time) + '秒')
                  time.sleep(stop_time)    
                  res = requests.get(url , headers = headers)
                  res.encoding = 'big5'
                  time.sleep(8 + random.uniform(0 , 1))
                  try: 
                      temp_unit = pd.read_html(StringIO(res.text))
                  except ValueError:
                      print('Mother fuck !!')
                      pass
              
              if len(temp_unit) > 1: 
                  
                  if season == 1:
                      season_date = datetime.date(year , 5 , 15)
                  elif season == 2:
                      season_date = datetime.date(year , 8 , 14)
                  elif season == 3:
                      season_date = datetime.date(year , 11 , 14)  
                  elif season == 4:
                      season_date = datetime.date(year , 3 , 31)  
                      
                  for kk in range(0 , 3):
                      temp_one_unit = temp_unit[kk + 1].iloc[2: , 0:2]
                      temp_one_unit = temp_one_unit.set_index([0])
                      temp_one_unit = temp_one_unit.apply(lambda s : pd.to_numeric(s , errors='coerce'))
                      temp_one_unit['INDEX'] = temp_one_unit.index
                      temp_one_unit = temp_one_unit.drop_duplicates(subset = 'INDEX', keep = 'last', inplace = False).drop('INDEX' , axis = 1)                                                      
                      temp_one_unit = temp_one_unit.reindex( table_list[kk] )
#                      temp_one_unit = temp_one_unit.loc[ table_list[kk] ]
                      temp_one_unit = temp_one_unit.T
                      temp_one_unit['date'] , temp_one_unit['證券代號'] = season_date , company[com]
                      temp_one_unit = temp_one_unit.set_index(['date','證券代號'])
                      temp_season[kk] = pd.concat([ temp_season[kk] , temp_one_unit ], axis = 0)
                      
                  print(str(year) + '-' + company[com] + '-' + '第' + str(season) + '季爬取完成')                          
                            
        balance_sheet = pd.concat([ balance_sheet , temp_season[0] ] , axis = 0)    
        financial_statements = pd.concat([ financial_statements , temp_season[1] ] , axis = 0)    
        cash_flow = pd.concat([ cash_flow , temp_season[2] ] , axis = 0)    
        
        print(str(year)+ '-' + company[com] + '-' + str(com) + '/' + str(len(company)))
            
conn = sqlite3.connect('stock_data.sqlite3')    
balance_sheet.to_sql('balance_sheet' , conn , if_exists = 'append')   
financial_statements.to_sql('financial_statements' , conn , if_exists = 'append')        
cash_flow.to_sql('cash_flow' , conn , if_exists = 'append') 


#----------------------伺服器不給連線的解決方法----------------------#
#from requests.exceptions import ConnectionError 一定要加這一行
#import requests
#try:
#   r = requests.get("http://example.com")
#except ConnectionError:
#   r = "No response"
#----------------------伺服器不給連線的解決方法----------------------#