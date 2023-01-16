# This function allows the user to input a database of tickers and output which one of them has the highest/lowest implied vol
# All implied vol data is based on the ATM option
# Returns a panda dataframe with sorted by leaders in IV of dataset

from main import tda_auth
import pandas as pd
import datetime


def get_iv_leaders(expiry,data='sp.csv'):
    vols = {}
    c = tda_auth()
    df = pd.read_csv(data)
    print(df)
    c.enforce_enums=False
    dte= datetime.datetime.strptime(expiry, '%Y-%m-%d').date()-datetime.date.today()
    for i in df['Symbol'].values:
        r = c.get_option_chain(i,strike_range='NTM')
        xx=r.json()['putExpDateMap'][expiry+":"+str(dte.days)]
        for z in xx:
            vols[i] = xx[z][0]['volatility'].__round__(2)
    finals = pd.DataFrame(vols.items(),columns=['Ticker','IV'])
    finals = finals.sort_values(by='IV',ascending=False)
    print(finals)
    return finals


get_iv_leaders('2023-02-17','sp.csv')