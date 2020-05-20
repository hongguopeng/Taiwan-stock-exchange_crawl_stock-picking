import pandas as pd
from finlab.data import Data
import datetime
data = Data()

data.date = datetime.date(2017,1,5)

price = data.get('收盤價' , 100)
股東權益 = data.get('歸屬於母公司業主之權益合計' , 1)
股本 = data.get('普通股股本' , 1)
pb = pd.DataFrame()
date = []
for i in range(0,1):
    if 股本.index[i] in price.index:
        pb_temp = price.loc[股本.index[i]] / (股東權益.loc[股本.index[i]] / (股本.loc[股本.index[i]] / 10))
        date_temp = datetime.datetime(股本.index[i].year , 股本.index[i].month , 股本.index[i].day)
    
    elif 股本.index[i] not in price.index:
        workday = datetime.datetime(股本.index[i].year , 股本.index[i].month , 股本.index[i].day)
        day = 股本.index[i].day
        while workday not in price.index:
            day = day + 1
            workday = datetime.datetime(股本.index[i].year , 股本.index[i].month , day)
        pb_temp = price.loc[workday] / (股東權益.loc[股本.index[i]] / (股本.loc[股本.index[i]] / 10))
        date_temp = workday
        
    pb = pd.concat([pb , pb_temp] , axis = 1)
    date.append(date_temp)
    
pb.columns = date
pb['證券代號'] = pb.index
pb.index = range(0,len(pb))
pb = pb.loc[pb.iloc[:,0].notnull()]
pb = pb.set_index('證券代號')
pb = pb.T
condition_pb = list(pb.columns[pb.iloc[0,:] < 0.5])

rev = data.get('當月營收', 12)
rev_近3月平均 = rev.iloc[-3: , :].mean(axis = 0) 
rev_年平均 = rev.mean(axis = 0) 
condition_rev = list(rev.columns[rev_近3月平均 > rev_年平均])

condition_pb_rev = list(set(condition_rev) & set(condition_pb))


# 簡易回測
data.date = datetime.date(2018,1,5)
price = data.get('收盤價' , 260)
price[condition_pb_rev].mean(axis = 1).plot()












