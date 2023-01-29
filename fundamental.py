from main import tda_auth
import pandas as pd
# initiliazes the request to authorize the API using the given dev code

def get_fundamental(file='sp.csv'):
    c=tda_auth()
    df=pd.read_csv(file) #insert data CSV here
    df=(df["Symbol"].tolist())
    c.enforce_enums=False
    r = c.search_instruments(df,'fundamental')
    data=r.json()
    stats=[]
    for i in data:
        # to save performance time, comment out data that you don't need
        pe=data[i]['fundamental']['peRatio'].__round__(2) #price to earnings ratio
        peg=data[i]['fundamental']['pegRatio'].__round__(2) #price to earnings-to-growth ratio
        pb=data[i]['fundamental']['pbRatio'].__round__(2) #price to book ratio
        pcf=data[i]['fundamental']['pcfRatio'].__round__(2) #price to cash flow ratio
        bvps=data[i]['fundamental']['bookValuePerShare'].__round__(2) #book value per share
        beta=data[i]['fundamental']['beta'] #beta ratio
        eps=data[i]['fundamental']['epsTTM'].__round__(2) #EPS trailing 12 months
        de=data[i]['fundamental']['totalDebtToEquity'].__round__(2) #debt to equity ratio
        h52=data[i]['fundamental']['high52'] #52 week high
        l52=data[i]['fundamental']['low52'] #52 week low
        div_perc=data[i]['fundamental']['dividendYield'] #dividend percentage yield
        volume=data[i]['fundamental']['vol3MonthAvg'] #average vol 3 months
        i={'ticker':i,'P/E':pe,'PEG':peg,'P/B':pb,'PCF':pcf,'BVPS':bvps,'Beta':beta,'EPS':eps,'D/E':de,'52H':h52,'52L':l52,'div_yield':div_perc,'3_month_vol':volume}
        stats.append(i)
    df= pd.DataFrame(stats) #returns pandas dataframe with all fundamental data
    return df

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d


def plot_fundamental_3d(file='sp.csv'):
    df = get_fundamental(file)
    # can change x,y,z values to whichever metric you prefer
    x=np.array(df['P/E'].values)
    y=np.array(df['P/B'].values)
    z=np.array(df['EPS'].values)
    # creates 3d plot axis and fig given x,y, and z values
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    plt.title("S&P 500")
    plt.xlabel("P/E")
    plt.ylabel("P/B")
    ax.scatter(x, y, z)
    ax.set_zlabel("EPS")
    plt.scatter(x,y,z)
    for x_l, y_l, z_l, label in zip(x, y, z, df['ticker']):
        ax.text(x_l, y_l, z_l, label)
    plt.show()

plot_fundamental_3d()