from main import tda_auth
import datetime
import matplotlib.pyplot as plt
import mplcyberpunk
ticker='F' #type symbol with all capitol letters ex. 'AAPL'
expiry='2023-03-17' #type str in YYYY-MM-DD format


def get_option_chain(ticker,expiry):
    c=tda_auth()
    start_date = datetime.datetime.strptime(expiry, '%Y-%m-%d').date()
    r = c.get_option_chain(ticker, contract_type=c.Options.ContractType.PUT, from_date=start_date,to_date=start_date,strike_count=100)
    underlying_price=(r.json()['underlyingPrice'])
    dte=start_date-datetime.date.today()
    xx=(r.json()['putExpDateMap'][expiry+":"+str(dte.days)])
    print(xx)
    vols={}
    deltas={}
    vegas={}
    thetas={}
    gammas={}
    for i in xx:
        vols[i]=xx[i][0]['volatility']
        deltas[i]=xx[i][0]['delta']
        vegas[i]=xx[i][0]['vega']
        thetas[i]=xx[i][0]['theta']
        gammas[i]=xx[i][0]['gamma']
    strikes=list(vols.keys())
    strikes=[float(x) for x in strikes]
    strikes=[int(x) for x in strikes]
    plt.style.use("cyberpunk")
    figure, axis = plt.subplots(2, 2)
    plt.setp(axis, xticks=strikes[::8])
    figure.suptitle(f"{ticker} {expiry}, {dte.days} DTE")
    #figure.suptitle(ticker+" data")

    # red vertical line is (x=current underlying price)
    axis[0,0].set_title("Vol Surface")
    axis[0,0].plot(strikes,vols.values())
    axis[0,0].axvline(underlying_price,color='red')
    axis[1,0].set_title("Delta")
    axis[1,0].plot(strikes,deltas.values(),color='orange')
    axis[1,0].axvline(underlying_price,color='red')
    axis[0,1].set_title("Theta")
    axis[0,1].plot(strikes,thetas.values(),color='violet')
    axis[0,1].axvline(underlying_price,color='red')
    axis[1,1].set_title("Gamma")
    axis[1,1].plot(strikes,gammas.values(),color='green')
    axis[1,1].axvline(underlying_price,color='red')
    plt.show()
get_option_chain(ticker,expiry)