
from auth.main import tda_auth
import pandas as pd
import datetime


def get_iv_leaders(expiry,data='sp.csv'):
    """
    Similar to iv_tracker function except it sorts them from greatest to smallest IV
    :param expiry: Expiration date to look at on the chain
    :param data: list of tickers to use in function; does NOT have to include price data just names
    :return:
    """
    vols = {}
    c = tda_auth()
    df = pd.read_csv(data,index_col=False)
    c.enforce_enums=False
    dte= datetime.datetime.strptime(expiry, '%Y-%m-%d').date()-datetime.date.today()
    for i in df['Symbol'].values:
        r = c.get_option_chain(i,strike_range='NTM')
        xx=r.json()['putExpDateMap'][expiry+":"+str(dte.days)]
        for z in xx:
            vols[i] = xx[z][0]['volatility'].__round__(2)
    finals = pd.DataFrame(vols.items(),columns=['Ticker','IV'])
    finals = finals.sort_values(by='IV',ascending=False,ignore_index=True)
    return finals




def iv_tracker(expiry,data,output_csv):
    """
    Function takes ATM IV of all given tickers at the given expiration date
    :param expiry: Enter valid expiration date for option chain
    :param data: Enter list of tickers to use in function; does NOT have to include price data just names
    :param output_csv: File that output will be appended to (.csv)
    :return: None
    """
    vols = {}
    c = tda_auth()
    df = pd.read_csv(data, index_col=False)
    c.enforce_enums = False
    dte = datetime.datetime.strptime(expiry, '%Y-%m-%d').date() - datetime.date.today()
    for i in df['Symbol'].values:
        r = c.get_option_chain(i, strike_range='NTM')
        xx = r.json()['putExpDateMap'][expiry + ":" + str(dte.days)]
        strikes = [float(x) for x in xx.keys()]
        index = str(float((min(strikes)+max(strikes))/2).__round__(0))
        if index in strikes:
            vols[i] = float(xx[index][0]['volatility'])
        else:
            index = str(float(strikes[int(len(strikes)/2)]))
            vols[i] = float(xx[index][0]['volatility'])
    finals = list(vols.values())
    df[str(datetime.date.today())]=finals
    df.to_csv(output_csv,index=False)


