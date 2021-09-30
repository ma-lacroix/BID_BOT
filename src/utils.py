# collection of tools to analyse stock information

import datetime
from typing import final
import pandas as pd
import numpy as np
import os
from pandas_datareader import data as dr
from pandas_datareader._utils import RemoteDataError
import csv
import os
import ctypes

def get_sp500():
    print("Getting list of S&P stock symbols...")
    # to rewrite in a bash script
    os.system('curl -LJO https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv')
    try:
        os.system('rm -r temp_data ')
        os.system('mkdir temp_data')
        os.system('mkdir results')
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
    residue = num%5
    incr = int((num-residue)/5)
    cnt = 0
    while(cnt<num-residue):
        print(f"Getting {cnt} to {cnt+incr-1}")
        df2 = get_close_prices(timeframe,security[cnt:cnt+incr])
        df = pd.concat([df2,df],axis=1)
        cnt+=incr
    if(residue>0):
        print(f"Getting {cnt} to {cnt+residue}")
        df2 = get_close_prices(timeframe,security[cnt:cnt+residue])['Close'].reset_index(drop=True,inplace=True)
        df.reset_index(drop=True,inplace=True)
        df = pd.concat([df2,df],axis=1)
    df.fillna(0,inplace=True)
    return df

def get_close_prices(timeframe,security):    
    service = 'yahoo'
    start = get_start(timeframe)
    end = datetime.datetime.today().strftime('%Y-%m-%d')    
    try:
        df = np.round(dr.DataReader(security,service,start,end),2)
        # df.sort_values('Date',inplace = True)
    except RemoteDataError:
        print("Data not found at Ticker {}".format(security))
    return df

def get_log_ret(intdict,symb_list):
    df = close_prices_loop(intdict,symb_list)
    df.to_csv('temp_data/daily_closes.csv')
    log_ret = pd.DataFrame(df['Close']/df['Close'].shift(1))
    # log_ret = pd.DataFrame(np.log(df/df.shift(1)))
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
    securities = pd.merge(securities,prices,on='Symbol',how='left')
    securities.to_csv('temp_data/securities.csv')
    return securities

def compile(libName,sourceFile):
    os.system("g++ --std=c++17 -shared -Wl,-install_name,{n}.so -o {n}.so -fPIC {s}.cpp "\
            "-I/Library/Frameworks/Python.framework/Versions/3.9/include/python3.9".format(n=libName,s=sourceFile))

def cpp_ratios(df,simulations):
    compile('cpp_sharpe','sharpe')
    cpp_sharpe = ctypes.CDLL('cpp_sharpe.so')
    dummy_returns = list(df.mean()*len(df))
    dummy_std = list(df.std()*len(df))
    arr_size = (ctypes.c_int)
    arr_size = len(dummy_std)
    arr1 = (ctypes.c_float*len(dummy_returns))(*dummy_returns)
    arr2 = (ctypes.c_float*len(dummy_std))(*dummy_std)
    cpp_sharpe.showSharpe(simulations,arr1,arr2,arr_size)

def gen_portolio(securities,simulations,sector):
    today = datetime.datetime.strftime(datetime.datetime.today(),'%Y-%m-%d')
    print("\nToday's date: {}\r".format(today))
    fdict = {'Symbol':[],'Share':[]}
    final_df = pd.DataFrame()
    try:
        log_returns = get_log_ret('3m',securities['Symbol'])
        cpp_ratios(log_returns,simulations)
        sol = open('temp_data/ratios.csv')
        r = csv.reader(sol)
        for row in zip(log_returns.columns[1:],r):
            fdict['Symbol'].append(row[0])
            fdict['Share'].append(row[1][0][0:4])
        final_df = pd.DataFrame.from_dict(fdict)
        final_df = pd.merge(final_df,securities,on='Symbol')[['Symbol','Share','Close','Name','Sector']].reset_index(drop=True)
        final_df.to_csv('results/portfolio_{}_{}.csv'.format(sector.lower().replace(' ','_'),today),index=False)
        print("Done producing optimal portfolio")
    except ValueError as error:
        print("Couldn't get Sharpe ratios - {}".format(error))

def update(sector):
    securities = get_sp500()
    securities = securities[securities['Sector']==sector]
    securities = trim_too_expensive(securities,100)
    gen_portolio(securities,100,sector)