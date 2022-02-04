import pandas as pd
import numpy as np
import yfinance as yf
from functions import change_char

### File with the NAFTRAC info
index_initial_comp = pd.read_csv("files/NAFTRAC_20200131.csv", skiprows =2)

### Table with only weights and Tickers
weights_initial = index_initial_comp.iloc[:-1,0:4:3]

### Cleanning the data to be readable by the yfinance library
Tickers = weights_initial.Ticker.map(change_char).map(lambda x: x.replace('.','-')).map(lambda x: x+'.MX')
weights_i = weights_initial[weights_initial.Ticker != "MXN"]
weights_i['Peso (%)'] = weights_i['Peso (%)']/100
weights_i.sort_values(by = 'Ticker',inplace=True)

#%% Section data Passive Investment

### Montly data from Jan-20
data_M = yf.download(tickers=Tickers[Tickers != "MXN.MX"].to_list(), start='2020-01-01', end= '2022-01-01', interval='1mo')
data_M = data_M['Adj Close'].dropna(axis=0)

#%% Section daily data Portfolio Weights
### Daily data from Jan-19 to Jan-20 
data_pre_d = yf.download(tickers=Tickers[Tickers != "MXN.MX"].to_list(), start='2019-01-01', end= '2020-01-31', interval='1d')
data_d = data_pre_d['Adj Close'].dropna(axis=0)

### Logarithmic returns of daily Adj Closed Prices
rend_d = np.log(data_d/data_d.shift(1)).dropna()

Returns_d = rend_d.mean()
Sigma_d = rend_d.cov()

#%% Section daily data Active Investment
data_act_d = yf.download(tickers=Tickers[Tickers != "MXN.MX"].to_list(), start='2019-01-01', end= '2020-01-31', interval='1d')
data_act_closes = data_act_d['Adj Close'].dropna(axis=0)

#%% Section constants

rf = 0.0429/252
capital = 1e6