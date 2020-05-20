import requests
import pandas as pd
import numpy as np
from io import StringIO
import os
import datetime
import sqlite3
    
start_year = 2014
start_month = 6
end_year = 2015
end_month = 6
year_month = [[start_year , start_month , 10]]
year = start_year
month = start_month
switch_on = 1

while switch_on == 1:
    month = month + 1    
    if month <= 12:
        year_month.append([year , month , 10])
    elif month > 12:
        month = 1
        year = year + 1
        year_month.append([year , month , 10])        
    if year == end_year and month == end_month:
        switch_on = 0
       
year_month = np.array(year_month)

data_all = pd.DataFrame()
for i in range(0 , len(year_month)):    
    
    url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_' + str(year_month[i,0] - 1911) + '_' + str(year_month[i,1]) + '_0.html'
    pseudo_broswer = {'user-agent' : 'Mozilla/5.0'}
    r = requests.get(url , headers = pseudo_broswer)     
    r.encoding = 'big5'
    
    datas = pd.read_html(StringIO(r.text))
    
    data_unit = pd.DataFrame()    
    if len(datas[0]) < 500:
        for j in range(0 , len(datas)):    
            if len(datas[j]) > 3 and j % 2 == 1:
                temp = datas[j].iloc[1 : -1 , 0 : -1]
                temp = temp.T
                temp = temp.set_index(1).T
                
                temp['date'] = np.zeros((len(temp) , 1)) 
                for k in range(0,len(temp)):
                    temp.iloc[k , -1] = datetime.datetime(year_month[i][0] , year_month[i][1] , year_month[i][2])
                temp['證券代號'] = temp['公司代號']
                temp = temp.set_index(['date' , '證券代號'])
                temp = temp.drop(columns=['公司名稱' , '公司代號'])
                temp = temp.apply(lambda s: pd.to_numeric(s, errors='coerce'))
                
                data_unit = pd.concat([data_unit , temp] , axis = 0)
            
    else:
        datas = datas[1:]
        for j in range(0 , len(datas)):
            if len(datas[j]) > 3 and j % 2 == 1:
                temp = datas[j].iloc[1 : -1 , 0 : -1]
                temp = temp.T
                temp = temp.set_index(1).T
                
                temp['date'] = np.zeros((len(temp) , 1)) 
                for k in range(0,len(temp)):
                    temp.iloc[k , -1] = datetime.datetime(year_month[i][0] , year_month[i][1] , year_month[i][2])
                temp['證券代號'] = temp['公司代號']
                temp = temp.set_index(['date' , '證券代號'])
                temp = temp.drop(columns=['公司名稱' , '公司代號'])
                temp = temp.apply(lambda s: pd.to_numeric(s, errors='coerce'))
                
                data_unit = pd.concat([data_unit , temp] , axis = 0)
    
    data_all = pd.concat([data_all , data_unit] , axis = 0)
    
    print('monthly_report_' + str(year_month[i][0]) + '_' + str(year_month[i][1]) + ' : Earn Money')
 
conn = sqlite3.connect('stock_data.sqlite3')
data_all.to_sql('monthly_report' , conn , if_exists = 'replace')




#---------------------------------另外一種寫法---------------------------------#
##if not os.path.isdir('每月月報資料夾'):
##	os.mkdir('每月月報資料夾')
#    
#start_year = 2015
#start_month = 1
#end_year = 2018
#end_month = 5
#year_month = [[start_year , start_month , 10]]
#year = start_year
#month = start_month
#switch_on = 1
#
#while switch_on == 1:
#    month = month + 1    
#    if month <= 12:
#        year_month.append([year , month , 10])
#    elif month > 12:
#        month = 1
#        year = year + 1
#        year_month.append([year , month , 10])        
#    if year == end_year and month == end_month:
#        switch_on = 0
#       
#year_month = np.array(year_month)
#
#data_all = pd.DataFrame()
#for i in range(0 , len(year_month)): 
##for i in range(0 , 1):      
#    
#    url = 'http://mops.twse.com.tw/nas/t21/sii/t21sc03_' + str(year_month[i,0] - 1911) + '_' + str(year_month[i,1]) + '_0.html'
#    pseudo_broswer = {'user-agent' : 'Mozilla/5.0'}
#    r = requests.get(url , headers = pseudo_broswer)     
#    r.encoding = 'big5'
#    
#    datas = pd.read_html(StringIO(r.text))
#    
#    data = datas[0]
#    data = data.iloc[:,0:10]
#    
#    columns_name = data.loc[data[0] == '公司代號' ]
#    columns_name = columns_name.iloc[0]
#    data.columns = columns_name
#    
#    data['公司代號'] = data['公司代號'].apply(lambda s: pd.to_numeric(s, errors='coerce'))
#    data = data.loc[data['公司代號'].notnull()]
#    
#    data['date'] = np.zeros((len(data),1))
#    for j in range(0,len(data)):
#          data.iloc[j , -1] = datetime.datetime(year_month[i][0] , year_month[i][1] , year_month[i][2])
#    
#    data['公司代號'] = data['公司代號'].apply(lambda s : str(s).replace('.0' , '')) 
#    data = data.drop(columns=['公司名稱']) 
#    data['證券代號'] = data['公司代號'] 
#    data = data.drop(columns=['公司代號']) 
#    data = data.set_index(['date','證券代號'])
#  
#    data = data.apply(lambda s: pd.to_numeric(s, errors='coerce'))
#    
#    data_all = pd.concat([data_all , data] , axis = 0)
#    
#    print('monthly_report_' + str(year_month[i][0]) + '_' + str(year_month[i][1]) + ' : Earn Money')
#
##    path = os.path.join('每月月報資料夾' , 'monthly_report' + year_month_save[0][i] + '_' + year_month_save[1][i] + '.csv' )  
##    data.to_csv(path, encoding = 'utf_8_sig')
#    
#conn = sqlite3.connect('stock_data.sqlite3')
#data_all.to_sql('monthly_report' , conn , if_exists = 'replace')
#---------------------------------另外一種寫法---------------------------------#        


