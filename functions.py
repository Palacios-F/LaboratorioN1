import pandas as pd
import numpy as np
from scipy.optimize import minimize 

def change_char(x:'String to me modify'):
    try:
        x = ''.join(ch for ch in x if ch not in ['*'])
    except:
        pass
    return x

def port_emv(Eind:"Vector with returns ", rf: "reference return free risk", Sigma: "Variance Covariance Matrix", r: "round digits"):
    """
    Functions that calculates the weights of Efficient Mean Variance Portfolio that takes 4 inputs
    ---
    return a vector with weights of the portfolio
    """
    n = len(Eind) 
    w0 = np.ones(n)/n
    bnds =((0,None),)*n
    cons = {'type':'eq','fun':lambda w: w.sum()-1}
    emv = minimize(fun = rs, x0=w0, args = (Eind,rf,Sigma,),
                 bounds = bnds, constraints = cons, tol = 1e-10)
    return np.round(emv.x,r)

def short_weigths(ind: "list of index", w: "weights"):
    """
    Function that return a dataframe with only the weights greaters than zero and Tickers
    """
    out = pd.DataFrame(index =ind, columns = ['Weights (%)'], data = w*100)
    outn = out.loc[out['Weights (%)']>0,:]
    return outn

def pasive(prices:"dataframe with prices", weights:"vector with weights", cash:"amount of cash", initial_capital:"initial amount of money"):
    """
    Function that calculates the pasive investment, take 4 inputs and returns a table with the result of the investment
    """
    cash_weights = (initial_capital)*weights #amount of money to be used in every commoditie
    n_sec = (cash_weights/prices.iloc[0,:]).round(0) #Number of titles
    cash = cash-sum([comission(n_sec[i],prices.iloc[0,i]) for i in range(len(n_sec))]) # cash after comssions
    amount = [(n_sec.to_numpy()).dot(prices.iloc[i,:].to_numpy()) for i in range(len(prices))]
    out = pd.DataFrame(index = prices.index,columns= ['Capital'],data = amount)
    out['Capital'] = out.Capital#correction with the cash 
    return out

def tabla_rend(data:"dataframe with capital"):
    data['rend'] =data.Capital.pct_change().fillna(0).round(6)
    data['rend_acum']= 100*((data.rend+1).cumprod()-1).round(6)
    data['rend'] = 100*data.rend
    return data

def active(prices:"dataframe with prices", weights:"vector with weights",rendi_d:"dataframe with daily returns", capital:"initial amount of money",thereshold:"activation level"):
    """
    Function that calculates the pasive investment, take 4 inputs and returns a table with the result of the investment
    """
    ##### calculations of the initial positions
    cash = capital # cash to use in purchases
    n_sec = np.zeros(len(weights)) #vector with number of securities
    com = 0 # commision quantity
    positions = rendi_d.T.loc[weights.index.to_list(),:].iloc[:,12].sort_values( ascending = False)#vector with daily returns sorted descending base on previous day 
    order = [rendi_d.T.loc[weights.index.to_list(),:].index.get_loc(positions.index[i]) for i in range(len(positions))]#list with index of securities based on daily returns 
    n_weights = weights.sort_index().iloc[:,0].to_numpy()/100 # vector with portfolio weights
    for posi in order:
        if (cash > 0) and (np.floor((capital*n_weights[posi]/prices.iloc[13,posi]))*prices.iloc[13,posi] < cash):
            n_sec[posi]=(np.floor((capital*n_weights[posi]/prices.iloc[13,posi])))
            cash = cash -1.00125*np.floor((capital*n_weights[posi]/prices.iloc[13,posi]))*prices.iloc[13,posi]
            com += comission(np.floor((capital*n_weights[posi]/prices.iloc[13,posi])),prices.iloc[13,posi])
        else: # case were there its no cash to cover all the positions 
            n_sec[posi]=(np.floor((0.99875*cash/prices.iloc[13,posi])))
            cash = cash -1.00125*np.floor((0.99875*cash/prices.iloc[13,posi]))*prices.iloc[13,posi]
            com += comission(np.floor((0.99875*cash/prices.iloc[13,posi])),prices.iloc[13,posi])
    
    ######## Calculations for the new portfolio weights
    returns = np.log(prices/prices.shift(1)).dropna() # dataframe with montly returns to determine the securitie to hold, seld or buy 
    wei = [n_sec]# list with positions 
    titles = [n_sec.sum()] # list with the total number of securities buy it per month
    commi = [com] # list with the total comission per month
    for i in range(12,len(returns)-1):
            sales = returns.columns[returns.iloc[i,:]< -1*thereshold]# securities that must be sold 
            index_sales = [returns.columns.get_loc(stock) for stock in sales]# index of securities to sold
            new_weights = np.zeros(len(n_weights))
            for j in index_sales:
                new_weights[j] = -np.floor(n_sec[j]*0.025)
                cash +=  np.floor(n_sec[j]*0.025)*prices.iloc[i+2,j]
            purchase = returns.columns[returns.iloc[i,:] > thereshold] # securities that must be buy
            index_purchase = [returns.columns.get_loc(stock) for stock in purchase]# index of securities to buy
            positions = rendi_d.T.loc[weights.index.to_list(),:].iloc[:,i+1].sort_values( ascending = False)
            order = [rendi_d.T.loc[weights.index.to_list(),:].index.get_loc(positions.index[ors]) for ors in range(len(positions))]
            purchase_order = [w for w in order if w  in index_purchase]
            nn_titles = 0#number of titles bought
            com = 0 #payed comissions 
            for j in purchase_order:
                if (cash > 0) and (np.floor(n_sec[j]*0.025)*prices.iloc[i+2,j] < cash):
                      new_weights[j] = np.floor(n_sec[j]*0.025)
                      nn_titles += np.floor(n_sec[j]*0.025)
                      cash += -np.floor(n_sec[j]*0.025)*prices.iloc[i+2,j]-comission(np.floor(n_sec[j]*0.025),prices.iloc[i+2,j])
                      com += comission(np.floor(n_sec[j]*0.025),prices.iloc[i+2,j])
                else:
                      new_weights[j] = np.floor(cash/prices.iloc[i+2,j])
                      nn_titles += np.floor(cash/prices.iloc[i+2,j])
                      cash += -np.floor(cash/prices.iloc[i+2,j])*prices.iloc[i+2,j]-comission(np.floor(cash/prices.iloc[i+2,j]),prices.iloc[i+2,j])
                      com += comission(np.floor(cash/prices.iloc[i+2,j]),prices.iloc[i+2,j])
            titles.append(nn_titles)
            commi.append(com)#month commisions 
            n_sec = n_sec + new_weights#new positions
            wei.append(n_sec)
    out = pd.DataFrame(index = prices.index[13:], data = np.multiply(np.array(wei),np.array(prices[13:])).sum(axis=1), columns = ['Capital'])#dataframe with portfolio's value
    df_titulos = pd.DataFrame(index = prices.index[13:],data={'titulos_comprados':titles,'comision':commi})#dataframe with commisions and number of securities
    df_titulos['titulos_totales'] = df_titulos['titulos_comprados'].cumsum()
    df_titulos['comision_acum'] = df_titulos['comision'].cumsum()
    return out,df_titulos

def medidas(active: "vector with rend active", pasive:"vector with rend pasive",sharpe_p,sharpe_a):
    prom_act = ((1+active.rend/100).cumprod()[-1])^(1/len(active))-1
    prom_pas = ((1+pasive.rend/100).cumprod()[-1])^(1/len(active))-1
    prom_act_c = ((1+active.rend/100).cumprod()[-1])-1
    prom_pas_c = ((1+pasive.rend/100).cumprod()[-1])-1
    sal = pd.DataFrame({'medida':['rend_m','rend_c','sharpe'],
                        'descripción':['Rendimiento Promedio Mensual','Rendimiento mensual acumulado','Sharpe Ratio'],
                        'inv_activa':[prom_act,prom_act_c,sharpe_a],
                        'inv_pasiva':[prom_pas,prom_pas_c,sharpe_p]})
    return sal

varianza = lambda w, Sigma: w.T.dot(Sigma).dot(w)
Sharpe = lambda er, s, rf: (er-rf)/s
rendimiento = lambda w, r: w.dot(r)
rs = lambda w,Eind,rf,Sigma: -(rendimiento(w,Eind)-rf)/ varianza(w,Sigma)**0.5
comission = lambda securitie,price: securitie*price*0.00125

