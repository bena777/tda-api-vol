# The purpose of this function is to display multiple vol surfaces across different expiries in order to compare and contrast the same strike implied vols for different expiry dates.
# Once again, TDA-dev keys and path will need to be specified from config.py file 
# Created by Ben Adelman, all data belongs to TDA
from tda import auth
import config
import datetime
import matplotlib.pyplot as plt
ticker='F'
expiries=[]
t=0

def get_data(ticker,expiry):
    global t
    #typical function used in other files to active the TDA auth and pull the chain
    try:
        c = auth.client_from_token_file(config.token_path, config.api_key)
    except FileNotFoundError:
        from selenium import webdriver

        with webdriver.Chrome(executable_path=config.chromedriver_path) as driver:
            c = auth.client_from_login_flow(
                driver, config.api_key, config.redirect_uri, config.token_path)
    start_date = datetime.datetime.strptime(expiry, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(expiry, '%Y-%m-%d').date()
    r = c.get_option_chain(ticker, contract_type=c.Options.ContractType.PUT,strike_count=str(50))
    underlying_price = (r.json()['underlyingPrice'])
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
        vols[i] = xx[i][0]['volatility'].__round__(0) #used in order to erase tick frequency; can edit to be more precise
        deltas[i] = xx[i][0]['delta']
        vegas[i] = xx[i][0]['vega']
        thetas[i] = xx[i][0]['theta']
        gammas[i] = xx[i][0]['gamma']

    strikes = list(vols.keys())
    strikes = [float(x) for x in strikes]
    strikes = [int(x) for x in strikes]
    plt.plot(strikes,vols.values(),label=expiry)
get_data(ticker,'2023-06-16') #used as placeholder so the function runs for the first time to grab the expiries
#loops the function for every expiry of the option
for i in expiries:
    get_data(ticker,i)
# plots labels, legend, and title
plt.xlabel("Strikes")
plt.ylabel("Vols")
plt.title(ticker+" vol surface")
plt.legend()
plt.show()
