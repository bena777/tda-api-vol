import numpy as np
from scipy.stats import norm
def blackscholes(St,K,v,t,r,typee):
    """
    Parameters:
    K : Excercise Price
    St: Current Stock Price
    v : Volatility in percentage
    r : Risk free rate in percentage
    t : Time to expiration in days
    typee: 'c' for call or 'p' for put
    © Ben A, Quantifiable 2022
    """
    t=t/365
    v=v/100
    r=r/100
    d1=(np.log(St/K)+((r+(np.power(v,2)/2))*t))/(v*np.sqrt(t))
    d2=d1-(v*np.sqrt(t))
    if typee=='c':
        N_d1=norm.cdf(d1)
        N_d2=norm.cdf(d2)
        n1 = (St * N_d1)
        n2 = (N_d2 * K)
        n3 = (np.exp(-r * t))
        price = n1 - (n2 * n3)
    else:
        N_d1=norm.cdf(-d1)
        N_d2=norm.cdf(-d2)
        n4=N_d2*(K*(np.exp(-r*t)))
        n5=N_d1*St
        price=n4-n5
    theta = (-((St * v * np.exp(-np.power(d1, 2) / 2)) / (np.sqrt(8 * np.pi * t))) + (d2 * r * K * np.exp(-r * t))) / 365
    gamma=(np.exp(-np.power(d1,2)/2))/(St*v*np.sqrt(2*np.pi*t))
    vega=(St*np.sqrt(t)*np.exp(-np.power(d1,2)/2))/(np.sqrt(2*np.pi)*100)
    return {'value':price,'nd2':N_d2,'delta':N_d1,'gamma':gamma,'theta':theta,'vega':vega}
