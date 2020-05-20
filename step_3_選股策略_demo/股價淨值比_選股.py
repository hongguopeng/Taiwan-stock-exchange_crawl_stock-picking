import pandas as pd
import numpy as np
from finlab.data import Data
import datetime


data = Data()
price = data.get('收盤價' , 1000)
股東權益 = data.get('歸屬於母公司業主之權益合計' , 8)
股本 = data.get('普通股股本' , 8)
 
pb = pd.DataFrame()
date = []
for i in range(0,8):
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
 

#bins = np.linspace(0 , 1 , num = 100)
#bins = list(bins) 
#pb.iloc[0].hist(bins = bins)


gain = price.iloc[-1] / price.loc[pb.index[0]]
gain = gain[pb.columns]
small_pb = pb.iloc[0] < 0.5 
gain_small_pb = gain[small_pb]


price_small_pb = price[pb.columns[small_pb]].loc[pb.index[0]:]
price_small_pb_mean = price_small_pb.mean(axis = 1)
price_small_pb_mean.plot()


























