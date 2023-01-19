# The purpose of this function is to display multiple vol surfaces across different expiries in order to compare and contrast the same strike implied vols for different expiry dates.
# Once again, TDA-dev keys and path will need to be specified from config.py file 
# Created by Ben A, all data belongs to TDA
from main import tda_auth
import datetime
import matplotlib.pyplot as plt
ticker='SPY'
expiries=[]
t=0
def get_vol_time_surface(ticker,expiry='2023-06-16'): #expiry used as placeholder to get program to run loop for first time
    c=tda_auth()
    global t
    start_date = datetime.datetime.strptime(expiry, '%Y-%m-%d').date()
    r = c.get_option_chain(ticker, contract_type=c.Options.ContractType.PUT,strike_count=str(50))
    dte = start_date - datetime.date.today()
    while t==0:
        for i in r.json()['putExpDateMap']:
            expiries.append(i[0:10])
            t=+1
    xx = (r.json()['putExpDateMap'][expiry + ":" + str(dte.days)])
    vols = {}
    deltas = {}
    vegas = {}
    thetas = {}
    gammas = {}
    for i in xx:
        vols[i] = xx[i][0]['volatility'] #used in order to erase tick frequency; can edit to be more precise
        deltas[i] = xx[i][0]['delta']
        vegas[i] = xx[i][0]['vega']
        thetas[i] = xx[i][0]['theta']
        gammas[i] = xx[i][0]['gamma']

    strikes = list(vols.keys())
    strikes = [float(x) for x in strikes]
    strikes = [int(x) for x in strikes]
    plt.plot(strikes,vols.values(),label=expiry)
get_vol_time_surface(ticker)
#loops the function for every expiry of the option
for i in expiries:
    get_vol_time_surface(ticker,i)
# plots labels, legend, and title in matplotlib
plt.xlabel("Strikes")
plt.ylabel("Vols")
plt.title(ticker+" vol surface")
plt.legend()
plt.show()
