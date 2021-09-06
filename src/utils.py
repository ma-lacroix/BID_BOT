# collection of tools to analyse stock information

import datetime
import pandas as pd
import numpy as np
import os
from pandas_datareader import data as dr
from pandas_datareader._utils import RemoteDataError

def get_sp500():
    print("Getting list of S&P stock symbols...")
    # to rewrite in a bash script
    os.system('curl -LJO https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv')
    try:
        os.system('rm -r temp_data ')
        os.system('mkdir temp_data')
    except:
        print("no such directory")
    os.system('mv constituents.csv temp_data/sp500.csv')
    df=pd.read_csv('temp_data/sp500.csv')
    return df

def get_securities_list(securities):
    symb_list = []
    for item in securities:
        symb_list.append(securities[item][1][0])
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
# minimizes the number of simultaneous stock price GET requests 
    print("Getting closing prices...")
    df = pd.DataFrame()
    num = len(security)
    residue = num%10
    incr = int((num-residue)/10)
    cnt = 0
    while(cnt<num-residue):
        print(f"Getting {cnt} to {cnt+incr-1}")
        df2 = get_close_prices(timeframe,security[cnt:cnt+incr]).reset_index(drop=True)
        print(df.head())
        df = pd.concat([df2,df],axis=1)
        cnt+=incr
    if(residue>0):
        print(f"Getting {cnt} to {cnt+residue}")
        df2 = get_close_prices(timeframe,security[cnt:cnt+residue]).reset_index(drop=True,inplace=True)
        df.reset_index(drop=True,inplace=True)
        df = pd.concat([df2,df],axis=1)
    df.fillna(0,inplace=True)
    return df

def get_close_prices(timeframe,security):    
    service = 'yahoo'
    start = get_start(timeframe)
    end = datetime.datetime.today().strftime('%Y-%m-%d')    
    try:
        df = np.round(dr.DataReader(security,service,start,end)['Close'],2)
        # df.sort_values('Date',inplace = True)
    except RemoteDataError:
        print("Data not found at Ticker {}".format(security))
    return df

def get_log_ret(intdict,symb_list):
    df = close_prices_loop(intdict,symb_list)
    # log_ret = pd.DataFrame(df['Close']/df['Close'].shift(1))
    log_ret = pd.DataFrame(np.log(df/df.shift(1)))
    log_ret.fillna(0,inplace=True)
    log_ret.to_csv('temp_data/returns.csv')
    return log_ret

def trim_too_expensive(securities,max_price):
    prices = close_prices_loop('1d',securities['Symbol'])['Close'].max().reset_index()
    prices.columns = ['Symbol','Close']
    print(f"Keeping stocks with open prices below {max_price}")
    for index,row in prices.iterrows():
        if(row['Close']>max_price):
            securities = securities[securities['Symbol']!=row['Symbol']]
    print("Total securities: {}".format(len(securities)))
    securities.to_csv('temp_data/securities.csv')
    return securities
