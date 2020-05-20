import datetime
import pandas as pd
import numpy as np
import sqlite3
import 讀取股市資料庫 as rs


#-------------------------匯入股市資料-------------------------#
conn = sqlite3.connect('stock_data.sqlite3')
data_all = pd.read_sql('select date , 證券代號, 收盤價 from "daily_price" ' , conn , index_col = ['date'])
data_all.index = pd.to_datetime(data_all.index , format = '%Y-%m-%d')
#-------------------------匯入股市資料-------------------------#




#-------------------------換股日期清單-------------------------# 
interval_day = 60  # interval_day代表幾天換一次股票
start = ['2016', '01' , '01']
end = ['2016' , '12' , '31']
start_date = datetime.date(int(start[0]) , int(start[1]) , int(start[2]))
end_date = datetime.date(int(end[0]) , int(end[1]) , int(end[2]))

while start_date not in data_all.index:
    start_date = start_date + datetime.timedelta(days = 1)
buy_date = [start_date]

temp_1 = start_date
switch_on = 1
while switch_on == 1:    
    temp_1 = temp_1 + datetime.timedelta(days = interval_day)
    if temp_1 < end_date:
        buy_date.append(temp_1)
    elif temp_1 >= end_date:
        switch_on = 0

sell_date = []        
for i in range(1 , len(buy_date)):
    temp_2 = buy_date[i] + datetime.timedelta(days = -1)
    sell_date.append(temp_2)
sell_date.append(end_date)  
#-------------------------換股日期清單-------------------------# 




#-------------------------股市資料準備-------------------------#    
data_interval = data_all.loc[start_date : end_date]
date = list(set(data_interval.index))
company = list(set(data_interval['證券代號']))
company = sorted(company)
target_data = pd.DataFrame()
for i in range(0,len(date)):    
    temp_1 = data_interval.loc[date[i]]
    temp_2 = temp_1   
    temp_2 = (temp_2.set_index(['證券代號'])).T
    temp_2['date'] = temp_1.index[0]
    temp_2 = temp_2.set_index(['date'])   
    target_data = pd.concat([target_data , temp_2] , axis = 0)
target_data = target_data.sort_index()  
#-------------------------股市資料準備-------------------------#




#-------------------------制定選股策略-------------------------#
def strategy_test(datedate):
    price = rs.daily_price(end = datedate , day = 200).sort_index()
    股本 = rs.seasonally_report_bs(select_date = datedate , target = ['股本合計'])
    當天股價 = pd.DataFrame( price.loc[:股本.index[0]].iloc[-1] )
    流通股數 = (股本 * 1000 / 10).T
    當天股價.columns , 流通股數.columns = range(0,1) , range(0,1)
    市值 = 流通股數 * 當天股價.loc[流通股數.index]
      
    pocket_list = 市值 < 5e9
    pocket_list = pocket_list.loc[pocket_list.iloc[:,0] == True]
      
    return pocket_list
#-------------------------制定選股策略-------------------------#




#-------------------------換股計算差價-------------------------#   
#target_data = target_data.T
#pocket_list = [1109 , 1231 , 1309 , 1323 ]  # 股票模擬清單，在實際執行中會依據買入日期時的選股條件做更換      
#pocket_list = pd.DataFrame(pocket_list).astype(str)
#target_data = target_data[pocket_list[1]] # 搜尋出股票模擬清單中的股價

spread = pd.DataFrame()
for j in range(0 , len(buy_date)):   
    pocket_list = strategy_test(datedate = buy_date[j])
    pocket_list_price = target_data[pocket_list.index[0 : 10]]
    
    buy_in = pocket_list_price.loc[ :buy_date[j] ].iloc[-1]
    sell_out = pocket_list_price.loc[ :sell_date[j] ].iloc[-1]
    spread = pd.concat([spread , sell_out - buy_in] , axis = 1) 
    print('\n' , spread)
spread_sum = pd.DataFrame(spread.sum(axis = 0))
spread_sum.index = range(0 , len(spread_sum))
spread_list = pd.concat([spread_sum , pd.DataFrame(buy_date) , pd.DataFrame(sell_date)] , axis = 1)
spread_list.columns = ['Spread' , 'Buy Date' , 'Sell Date']
#-------------------------換股計算差價-------------------------#     




#---------總資金 1000000元，依照今天收盤價，股票張數要如何分配---------#
stock_list = data_all.loc[data_all.index[-1]] # 選擇最新一天的股價
stock_list = stock_list.set_index(['證券代號'])
stock_list = stock_list.loc[pocket_list.index]
money = 1000000  # 資金
lowest_fee = 20  # 最低手續費
discount = 0.28  # 手續費折扣，各家證券公司都不同
add_cost = 10    # 若覺得自己沒辦法負荷這麼多檔股票可以加大這個值，股票張數就不會這麼多

print('estimate price according to', str(data_all.index[-1])[0 : -9])

print('initial number of stock', len(stock_list))

test = stock_list
# 買下每張股票平均所需花費的手續費要超過20塊，就不用考慮不足20塊還要還要以20塊算的問題
# (money / len(stock_list)) * (1.425 / 1000) * discount => 平均一張股票的手續費
# AA.loc[BB] => BB要是Series，不能是DataFrame
while (money / len(stock_list)) * (1.425 / 1000) * discount < (lowest_fee - add_cost): 
    stock_list = stock_list.loc[(stock_list != stock_list.max()).iloc[: , 0]]
   
print('after considering fee', len(stock_list))
    
while True:
    invest_amount = (money / len(stock_list))
    ret = np.floor(invest_amount / 1000 / stock_list)
    if (ret == 0).any().iloc[0]:
        stock_list = stock_list.loc[(stock_list != stock_list.max()).iloc[: , 0]]
    else:
        break
# ret最後代表每張股票可以買的張數

print('after considering 1000 share', len(stock_list))
    
final_total_invest_amount = (ret * stock_list * 1000).sum()  
#---------給定 1000000元，依照今天收盤價，股票張數要如何分配---------#

