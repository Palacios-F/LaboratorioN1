import pandas as pd
import numpy as np
import yfinance as yf
import os
from functions import change_char

### File with the NAFTRAC info
index_initial_comp = pd.read_csv("files/NAFTRAC_20200131.csv", skiprows =2)

docs = os.listdir(os.getcwd()+"\\files")

csvfile = {document :pd.read_csv("files/" + document,
                                 skiprows = 2,nrows=39).iloc[:,0].to_list() + [""]*(39-len(pd.read_csv("files/" + document,
                                 skiprows = 2,nrows=39).iloc[:,0].to_list())) for document in docs}
csvfile = pd.DataFrame(data = csvfile)
df1 = csvfile.melt(var_name='columns', value_name='index')
df2 = pd.crosstab(index=df1['index'], columns=df1['columns'])
df3 = df2.sum(axis=1)

dates = [doc[8:12] + "-"+ doc[12:14] + "-" + doc[14:16] for doc in docs]

### Table with only weights and Tickers
weights_initial = index_initial_comp.iloc[:-1,0:4:3]

### Cleanning the data to be readable by the yfinance library
Tickers = weights_initial.Ticker.map(change_char).map(lambda x: x.replace('.','-')).map(lambda x: x+'.MX')
weights_i = weights_initial[(((weights_initial.Ticker != "MXN") & (weights_initial.Ticker != "KOFUBL")) & (weights_initial.Ticker != "BSMXB"))]            
weights_i['Peso (%)'] = weights_i['Peso (%)']/100
weights_i.sort_values(by = 'Ticker',inplace=True)
list_weights = weights_i.iloc[:,1].to_numpy()

#%% Section data Passive Investment

### Montly data from Jan-20
#data_M = yf.download(tickers=Tickers[Tickers != "MXN.MX"].to_list(), start='2020-01-01', end= '2022-01-01', interval='1mo')
#data_M = data_M['Adj Close'].dropna(axis=0)

#%% Section daily data Portfolio Weights
### Daily data from Jan-19 to Jan-20 
data_pre_d = yf.download(tickers=Tickers[Tickers != "MXN.MX"].to_list(), start='2019-01-01', end= '2020-01-31', interval='1d')
data_d = data_pre_d['Adj Close'].dropna(axis=0)

### Logarithmic returns of daily Adj Closed Prices
rend_d = np.log(data_d/data_d.shift(1)).dropna()

Returns_d = rend_d.mean()
Sigma_d = rend_d.cov()

#%% Section daily data Active Investment
data_act_d = yf.download(tickers=Tickers[Tickers != "MXN.MX"].to_list(), start='2020-01-31', end= '2022-01-27', interval='1d')
data_act_closes = data_act_d['Close'].dropna(axis=0)
data_rend_closes = data_act_closes.pct_change().dropna()
closes_rend_dates = data_rend_closes[np.roll(data_rend_closes.index.isin(dates),-1)]
### data corresponding to end of month 
data_M = data_act_closes.loc[dates,:]




#%% Section constants

rf = 0.0429/252
capital = 1000000
cash = capital*weights_initial.iloc[34,1]/100+capital*weights_initial.iloc[10,1]/100+capital*weights_initial.iloc[32,1]/100

example = data_M.loc[:,~data_M.columns.isin(['KOFUBL.MX','BSMXB.MX'])]

#results_pasive = pasive(data_M.loc[:,~data_M.columns.isin(['KOFUBL.MX','BSMXB.MX'])],list_weights,
#                            cash, capital)
#results_pasive = tabla_rend(results_pasive)

#nuevo =np.log(example/example.shift(1)).dropna()

#efficient_w = fun.port_emv(Returns_d,rf,Sigma_d,4)
#weights_sharpe = short_weigths(Tickers[Tickers != "MXN.MX"].to_list(),efficient_w)


