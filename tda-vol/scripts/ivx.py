import pandas as pd
from main import tda_auth
from datetime import datetime
import numpy as np


def linear_interp_list(y):
    df = pd.Series(y)
    df = df.replace("NaN",np.nan)
    df = df.interpolate(limit_area='inside')
    return list(df.values)

def ivx_calculation(ticker,front):
    """
    :param ticker:
    :param front month expiration date (Must be over 7DTE):
    Calculates the IVx of inputted ticker in TastyTrade style way
    IVx serves a similar function as the VIX index except it can be calculated on any underlying
    However, it works better on liquid assets as all NaN values are linearly interpolated
    Weights ATM options at 0.4 and cuts each +-i in half each time (weights subject to change)
    Created by Ben A
    """
    c = tda_auth()
    c.enforce_enums=False
    r = c.get_option_chain(symbol=ticker)
    price = c.get_quote(ticker).json()[ticker]['lastPrice']
    today = datetime.today().date()
    dte_front=(datetime.strptime(front,'%Y-%m-%d').date()-today).days
    atm_option = 0
    dif=1000
    for x in list(r.json()['callExpDateMap'][front+":"+str(dte_front)]):
        if abs(float(x)-price)<dif:
            dif=abs(float(x)-price)
            atm_option=x
    front_chain_c=r.json()['callExpDateMap'][str(front)+":"+str(dte_front)]
    ivx_front=0
    vols = [i[0]['volatility'] for i in list(front_chain_c.values())]
    strikes = list(front_chain_c.keys())

    atm_index = strikes.index(str(float(atm_option)))
    starting_factor = 0.3 #factor for splitting weights (should be 0.3)
    factor = starting_factor/2
    sum = starting_factor+0.1 #+0.1 is used to make it equal 1 as other
    ivx_front += vols[atm_index]*(starting_factor+0.1)

    vols = linear_interp_list(vols) #interpolate NaN values
    for i in range(1,atm_index): #can adjust to accomidate for more or less options
        sum+=factor*2
        ivx_front += ((vols[atm_index+i]*factor) + (vols[atm_index-i]*factor)) #actually works and is more efficient but now need to work on actual methodlogy
        factor = factor / 2
    ivx=ivx_front
    return ivx
