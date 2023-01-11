from tda import auth
import config
import pandas as pd

# initiliazes the request to authorize the API using the given dev code

try:
    c = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path=config.chromedriver_path) as driver:
        c = auth.client_from_login_flow(
            driver, config.api_key, config.redirect_uri, config.token_path)
c.enforce_enums=False
df=pd.read_csv("sp.csv") #insert data CSV here
df=(df["Symbol"].tolist())
r = c.search_instruments(df,'fundamental')
data=r.json()
stats=[]
for i in data:
    pe=data[i]['fundamental']['peRatio'] #price to earnings ratio
    peg=data[i]['fundamental']['pegRatio'] #price to earnings-to-growth ratio
    pb=data[i]['fundamental']['pbRatio'] #price to book ratio
    pcf=data[i]['fundamental']['pcfRatio'] #price to cash flow ratio
    bvps=data[i]['fundamental']['bookValuePerShare'] #book value per share
    beta=data[i]['fundamental']['beta'] #beta ratio
    eps=data[i]['fundamental']['epsTTM'] #EPS trailing 12 months
    de=data[i]['fundamental']['totalDebtToEquity'] #debt to equity ratio
    h52=data[i]['fundamental']['high52'] #52 week high
    l52=data[i]['fundamental']['low52'] #52 week low
    div_perc=data[i]['fundamental']['dividendYield'] #dividend percentage yield
    vol=data[i]['fundamental']['vol3MonthAvg'] #average vol 3 months
    i={'ticker':i,'P/E':pe,'PEG':peg,'P/B':pb,'PCF':pcf,'BVPS':bvps,'Beta':beta,'EPS':eps,'D/E':de,'52H':h52,'52L':l52,'div_yield':div_perc,'3_month_vol':vol}
    stats.append(i)

df= pd.DataFrame(stats) #returns pandas dataframe with all fundamental data
