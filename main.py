#import sys
#!{sys.executable} -m pip install -r requirements.txt

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import data as dt

#%%
import functions as fun
import visualizations as vs

#%% Pasive Investment
results_pasive = fun.pasive(dt.data_M,dt.weights_i.iloc[:,1].to_numpy(), dt.capital*dt.weights_initial.iloc[34,1], dt.capital)
results_pasive = fun.tabla_rend(results_pasive)


#%% Active Investment
efficient_w = fun.port_emv(dt.Returns_d,dt.rf,dt.Sigma_d,4)
weights_sharpe = fun.short_weigths(dt.Tickers[Tickers != "MXN.MX"].to_list(),efficient_w)

#%%
vs.pie_com(example)
vs.returns_plot(results_pasive)