from finlab.data import Data
import pandas as pd

data = Data()

#--------------------------------------------------------------#

股本 = data.get('股本合計', 1)
price = data.get('收盤價', 100)

當天股價 = pd.DataFrame( price.loc[:股本.index[0]].iloc[-1] )

流通股數 = (股本 * 1000 / 10).T
市值 = 流通股數 * pd.DataFrame(當天股價.loc[流通股數.index])

#--------------------------------------------------------------#

def unit_season(data_累積):
    data_單季 = pd.DataFrame()
    for i in range(0 , len(data_累積)):
        if i != 0 and data_累積.index[i].month != 5:   
            temp = data_累積.iloc[i , :] - data_累積.iloc[i - 1 , :]
            temp = pd.DataFrame(temp).T
            data_單季 = pd.concat([data_單季 , temp] , axis = 0)
        if data_累積.index[i].month == 5 or i == 0:
            temp = data_累積.iloc[i , :]
            temp = pd.DataFrame(temp).T
            data_單季 = pd.concat([data_單季 , temp] , axis = 0)
    data_單季['date'] = data_累積.index
    data_單季 = data_單季.set_index(['date'])
    return data_單季 

營業現金流_累積 = data.get('營業活動之淨現金流入（流出）', 8)
營業現金流_單季 = unit_season(營業現金流_累積 )
投資現金流_累積 = data.get('投資活動之淨現金流入（流出）', 8)
投資現金流_單季 = unit_season(投資現金流_累積 )
自由現金流 = (營業現金流_單季 + 投資現金流_單季).iloc[-4:].sum()  

#--------------------------------------------------------------#   

稅後淨利 = data.get('本期淨利（淨損）', 1)
權益總計 = data.get('權益總計', 1)
權益總額 = data.get('權益總額', 1)
權益總計.fillna(權益總額, inplace=True)
股東權益報酬率 = 稅後淨利.iloc[-1] / 權益總計.iloc[-1]

#--------------------------------------------------------------# 

營業利益 = data.get('營業利益（損失）', 5)
營業利益年成長率 = (營業利益.iloc[-1] / 營業利益.iloc[-5] - 1) * 100

#--------------------------------------------------------------# 

當月營收 = data.get('當月營收', 4) * 1000
當季營收 = (pd.DataFrame(當月營收.iloc[-4:].sum())).T
當季營收['date'] = 市值.columns
當季營收 = (當季營收.set_index(['date'])).T
市值營收比 = 市值.loc[當季營收.index] / 當季營收

#--------------------------------------------------------------#

def form_dataframe(df):
      df = (pd.DataFrame(df)).T
      df['ADD'] = range(0,1)
      df = (df.set_index(['ADD'])).T
      return df

condition1 = form_dataframe(市值 < 10000000000)
condition2 = form_dataframe(自由現金流 > 0)
condition3 = form_dataframe(股東權益報酬率 > 0)
condition4 = form_dataframe(營業利益成長率 > 0)
condition5 = form_dataframe(市值營收比 < 5)
select_stock = condition1 & condition2 & condition3 & condition4 & condition5 
select_stock = select_stock.loc[select_stock.iloc[:,0] == True]
