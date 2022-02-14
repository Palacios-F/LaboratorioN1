#import sys
#!{sys.executable} -m pip install -r requirements.txt
import data as dt
import functions as fun
import visualizations as vs

#%% Pasive Investment
results_pasive = fun.pasive(dt.data_M.loc[:,~dt.data_M.columns.isin(['KOFUBL.MX','BSMXB.MX'])],dt.list_weights,
                            dt.cash, dt.capital)
results_pasive = fun.tabla_rend(results_pasive)

print("Los resultados de la estrategia pasiva son los siguientes: ")
print(results_pasive)
#%% Active Investment
efficient_w = fun.port_emv(dt.Returns_d,dt.rf,dt.Sigma_d,4)
weights_sharpe = fun.short_weigths(dt.Tickers[dt.Tickers != "MXN.MX"].to_list(),efficient_w)

results_active, table_T = fun.active(dt.data_M.loc[:,dt.data_M.columns.isin(weights_sharpe.index.sort_values().to_list())],
                             weights_sharpe,dt.closes_rend_dates,dt.capital,0.05)
results_active = fun.tabla_rend(results_active)

print("Los resultados de la estrategia activa son los siguientes: ")
print(results_active)

print("la tabla con los movimientos de los títulos es la siguiente: ")
print(table_T)
#%%
#vs.pie_com(example)
#vs.returns_plot(results_pasive)

