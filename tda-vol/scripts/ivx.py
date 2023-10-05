from main import tda_auth
from datetime import datetime
def ivx_calculation(ticker,front):
    """
    :param ticker:
    :param front month expiration date (Must be over 7DTE):
    :param back month expiration date:
    Calculates the IVx of inputted ticker in TastyTrade style way
    IVx serves a similar function as the VIX index except it is only based on ATM/ near ATM optiopns leading to it being able to be done on ANY optionable security
    Weights ATM options at 60%, +-1 at 30%, and +-2 at 10%
    This is done for both options, and they are then simply averaged to return the IVX
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
    front_chain_p=r.json()['putExpDateMap'][str(front)+":"+str(dte_front)]
    ivx_front=0
    vols_c = [i[0]['volatility'] for i in list(front_chain_c.values())]
    strikes = list(front_chain_c.keys())
    vols_p = [i[0]['volatility'] for i in list(front_chain_p.values())]

    atm_index = strikes.index(str(float(atm_option)))

    ivx_front += (vols_c[atm_index]*0.6 + vols_c[atm_index+1]*0.3 + vols_c[atm_index-1]*0.1) #actually works and is more efficient but now need to work on actual methodlogy
    ivx_front += (vols_p[atm_index]*0.6 + vols_p[atm_index+1]*0.3 + vols_p[atm_index-1]*0.1)

    ivx=(ivx_front/2)
    return ivx
