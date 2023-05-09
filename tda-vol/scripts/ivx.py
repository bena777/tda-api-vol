
from auth.main import tda_auth
from datetime import datetime
def ivx_calculation(ticker,front,back):
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
    if dte_front<=7:
        raise TypeError("Expiration must be more than a week out")
    dte_back=(datetime.strptime(back,'%Y-%m-%d').date()-today).days
    atm_option = 0
    dif=1000
    for x in list(r.json()['callExpDateMap'][front+":"+str(dte_front)]):
        if abs(float(x)-price)<dif:
            dif=abs(float(x)-price)
            atm_option=x
    front_chain_c=r.json()['callExpDateMap'][str(front)+":"+str(dte_front)]
    front_chain_p=r.json()['putExpDateMap'][str(front)+":"+str(dte_front)]
    back_chain_c=r.json()['callExpDateMap'][str(back)+":"+str(dte_back)]
    back_chain_p=r.json()['putExpDateMap'][str(back)+":"+str(dte_back)]
    ivx_front=0
    ivx_back=0

    ivx_front+=(front_chain_c[atm_option][0]['volatility']*0.6)+(front_chain_c[str(float(atm_option)+1)][0]['volatility']*0.3)+(front_chain_c[str(max(front_chain_c.keys()))][0]['volatility']*0.1)
    ivx_front+=(front_chain_p[atm_option][0]['volatility']*0.6)+(front_chain_p[str(float(atm_option)-1)][0]['volatility']*0.3)+(front_chain_c[str(max(front_chain_c.keys()))][0]['volatility']*0.1)
    ivx_back+=(back_chain_c[atm_option][0]['volatility']*0.6)+(back_chain_c[str(float(atm_option)+1)][0]['volatility']*0.3)+(back_chain_c[str(float(atm_option)+2)][0]['volatility']*0.1)
    ivx_back+=(back_chain_p[atm_option][0]['volatility']*0.6)+(back_chain_p[str(float(atm_option)-1)][0]['volatility']*0.3)+(back_chain_c[str(float(atm_option)-2)][0]['volatility']*0.1)
    ivx=(ivx_front/2)
    return ivx
