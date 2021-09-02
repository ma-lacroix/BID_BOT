# collection of tools to analyse stock information

import datetime
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import sharpe,recommendations

def get_sp500():
    print("Getting list of S&P stock symbols...")        
    df=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0][['GICS Sub-Industry','GICS Sector','Symbol']]
    df=df[df['Symbol']!='GOOG'].reset_index(drop=True) # removing some stocks
    return df.head(500)

def check_dtype_securities(securities):
# different data types will flow through the program
    if(type(securities)==dict):
        symb_list = recommendations.get_securities_list(securities)
    elif(type(securities)==list):
        symb_list = securities
    elif(type(securities)==pd.core.frame.DataFrame):
        symb_list = securities['Symbol']
    else:
        print("Wrong stock symbols data type - must be a list of dict")
        symb_list = []
    return symb_list

def get_start(timeframe):
    if(timeframe=='1d'):
        start = (datetime.datetime.today()-datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    elif(timeframe=='1w'):
        start = (datetime.datetime.today()-datetime.timedelta(days=8)).strftime('%Y-%m-%d')
    elif(timeframe=='1m'):
        start = (datetime.datetime.today()-datetime.timedelta(days=31)).strftime('%Y-%m-%d')
    elif(timeframe=='3m'):
        start = (datetime.datetime.today()-datetime.timedelta(days=93)).strftime('%Y-%m-%d')
    else:
        start = datetime.datetime.today().strftime('%Y-%m-%d')
    return start

def close_prices_loop(timeframe,security):
# minimizes the number of simultaneous price requests 
    print("Getting closing prices...")
    df = pd.DataFrame()
    num = len(security)
    residue = num%10
    incr = int((num-residue)/10)
    cnt = 0
    while(cnt<num-residue):
        print(f"Getting {cnt} to {cnt+incr-1}")
        df = pd.concat([get_close_prices(timeframe,security[cnt:cnt+incr]),df])
        cnt+=incr
    if(residue>0):
        print(f"Getting {cnt} to {cnt+residue}")
        df = pd.concat([get_close_prices(timeframe,security[cnt:cnt+residue]),df])
    df.fillna(0,inplace=True)
    return df

def get_close_prices(timeframe,security):    
    service = 'yahoo'
    start = get_start(timeframe)
    end = datetime.datetime.today().strftime('%Y-%m-%d')    
    try:
        df = np.round(web.DataReader(security,service,start,end)[['Close','Volume']],2)
        df.sort_values('Date',inplace = True)
    except ValueError as error:
        print("Couldn't connect to {} - {}".format(service,error))
    return df

def trim_too_expensive(securities,max_price):
    symb_list = check_dtype_securities(securities)
    prices = close_prices_loop('1d',symb_list)['Close'].max().reset_index()
    prices.columns = ['Symbol','Close']
    print(f"Keeping stocks with open prices below {max_price}")
    for index,row in prices.iterrows():
        if(row['Close']>max_price):
            securities = securities[securities['Symbol']!=row['Symbol']]
    print("Total securities: {}".format(len(securities)))
    return securities
