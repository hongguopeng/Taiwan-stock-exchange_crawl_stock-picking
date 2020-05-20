import requests
from requests.exceptions import ConnectionError
import pandas as pd
import numpy as np
import time
import datetime
from io import StringIO
import random
import os

start_year = 2017
end_year = 2018
now = datetime.datetime.now()

bs_item = []
fs_item = []
cf_item = []

for year in range(start_year , end_year):      
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
          
            temp_bs_season = pd.DataFrame()
            for season in range(1,5):
                  
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
                          print('What the fuck !!')
                          pass
                  
                  if len(temp_unit) > 1: 
                      bs_item = bs_item + list(temp_unit[1].iloc[2: , 0])
                      bs_item = sorted(set(bs_item))  
                      
                      fs_item = fs_item + list(temp_unit[2].iloc[2: , 0])
                      fs_item = sorted(set(fs_item))
                      
                      cf_item = cf_item + list(temp_unit[3].iloc[2: , 0])
                      cf_item = sorted(set(cf_item))
                 
                  print(str(year) + '-' + company[com] + '-' + '第' + str(season) + '季爬取成功')          
 
                    
bs_item = sorted(set(bs_item))
path = os.path.join('bs_item.txt')
bs = open(path, 'w+')
for i in range(0 , len(bs_item)):
    bs.write(bs_item[i] + '\n')
bs.close() 
                       
fs_item = sorted(set(fs_item))
path = os.path.join('fs_item.txt')
fs = open(path, 'w+')
for j in range(0 , len(fs_item)):
    fs.write(fs_item[j] + '\n')
fs.close() 
 
cf_item = sorted(set(cf_item))
path = os.path.join('cf_item.txt')
cf = open(path, 'w+')
for k in range(0 , len(cf_item)):
    cf.write(cf_item[k] + '\n') 
cf.close() 

