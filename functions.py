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
    cash_weights = (initial_capital - cash)*weights #amount of money to be used in every commoditie
    n_sec = np.ceil(cash_weights/prices.iloc[0,:]) #Number of titles
    cash = cash-sum([comission(n_sec[i],prices.iloc[0,i]) for i in range(len(n_sec))]) # cash after comssions
    amount = [(n_sec.to_numpy()).dot(prices.iloc[i,:].to_numpy()) for i in range(len(prices))]
    out = pd.DataFrame(index = prices.index,columns= ['Capital'],data = amount)
    out['Capital'] = out.Capital + cash #correction with the cash 
    return out

def tabla_rend(data:"dataframe with capital"):
    data['rend'] =data.Capital.pct_change().fillna(0)
    data['rend_acum']= (data.rend+1).cumprod()-1
    return data

def active(weights):
    return weights

varianza = lambda w, Sigma: w.T.dot(Sigma).dot(w)
Sharpe = lambda er, s, rf: (er-rf)/s
rendimiento = lambda w, r: w.dot(r)
rs = lambda w,Eind,rf,Sigma: -(rendimiento(w,Eind)-rf)/ varianza(w,Sigma)**0.5

comission = lambda securitie,price: securitie*price*0.00125
