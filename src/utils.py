# collection of tools to analyse stock information

import datetime
import time
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
        start = (datetime.datetime.today()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    elif(timeframe=='1w'):
        start = (datetime.datetime.today()-datetime.timedelta(days=8)).strftime('%Y-%m-%d')
    elif(timeframe=='1m' or timeframe=='1mago'):
        start = (datetime.datetime.today()-datetime.timedelta(days=31)).strftime('%Y-%m-%d')
    elif(timeframe=='3m' or timeframe=='3mago'):
        start = (datetime.datetime.today()-datetime.timedelta(days=93)).strftime('%Y-%m-%d')        
    elif(timeframe=='6m' or timeframe=='6mago'):
        start = (datetime.datetime.today()-datetime.timedelta(days=186)).strftime('%Y-%m-%d')
    else:
        start = datetime.datetime.today().strftime('%Y-%m-%d')
    return start

def close_prices_loop(timeframe,security):
# minimizes the number of simultaneous stock price GET requests 
    print("Getting closing prices for the last {}...".format(timeframe))
    df = pd.DataFrame()
    num = len(security)
    residue = num%5
    incr = int((num-residue)/5)
    cnt = 0
    timestart = datetime.datetime.now()
    while(cnt<num-residue):
        df2 = get_close_prices(timeframe,security[cnt:cnt+incr])
        df = pd.concat([df2,df],axis=1)
        time.sleep(2.0) # adding small buffer
        cnt+=incr
    if(residue>0):
        df2 = get_close_prices(timeframe,security[cnt:cnt+residue+1])
        time.sleep(2.0) # adding small buffer
        df = pd.concat([df2,df],axis=1)
    df.fillna(0,inplace=True)
    timeend = datetime.datetime.now()
    print("\nRun time: {}".format((timeend-timestart).total_seconds()))
    return df

def get_close_prices(timeframe,security):    
    service = 'yahoo'
    start = get_start(timeframe)
    if(timeframe=='3mago'):
        end = (datetime.datetime.today()-datetime.timedelta(days=89)).strftime('%Y-%m-%d')
    elif(timeframe=='1mago'):
        end = (datetime.datetime.today()-datetime.timedelta(days=27)).strftime('%Y-%m-%d')
    else:
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
    log_ret = pd.DataFrame(df['Close']/df['Close'].shift(1)-1)
    # log_ret = pd.DataFrame(np.log(df/df.shift(1)))
    log_ret.fillna(0,inplace=True)
    log_ret.to_csv('temp_data/returns.csv')
    return log_ret

def trim_too_expensive(securities,max_price):

    prices = close_prices_loop('1d',securities['Symbol'])['Close'].max().reset_index()
    prices.columns = ['Symbol','Close']
    prices3m = close_prices_loop('3mago',securities['Symbol'])['Close'].max().reset_index()
    prices3m.columns = ['Symbol','Close']
    prices3m.rename({'Close':'Close3m'},axis=1,inplace=True)
    prices1m = close_prices_loop('1mago',securities['Symbol'])['Close'].max().reset_index()
    prices1m.columns = ['Symbol','Close']
    prices1m.rename({'Close':'Close1m'},axis=1,inplace=True)

    print(f"Keeping stocks with open prices below {max_price}")
    for index,row in prices.iterrows():
        if(row['Close']>max_price):
            securities = securities[securities['Symbol']!=row['Symbol']]
    print("Total securities: {}".format(len(securities.index)))
    securities = pd.merge(securities,prices,on='Symbol',how='inner')
    
    securities = pd.merge(securities,prices3m,on='Symbol',how='inner')
    securities = pd.merge(securities,prices1m,on='Symbol',how='inner')
    securities.to_csv('temp_data/securities.csv')
    
    return securities

def compile(libName,sourceFile):
    os.system("g++ --std=c++17 -shared -Wl,-install_name,{n}.so -o {n}.so -fPIC {s}.cpp "\
            "-I/Library/Frameworks/Python.framework/Versions/3.9/include/python3.9".format(n=libName,s=sourceFile))

def cpp_ratios(df,simulations):
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
    fdict = {'yyyy_mm_dd':[],'Symbol':[],'Share':[]}
    final_df = pd.DataFrame()
    try:
        log_returns = get_log_ret('3m',securities['Symbol'])
        cpp_ratios(log_returns,simulations)
        sol = open('temp_data/ratios.csv')
        r = csv.reader(sol)
        for row in zip(log_returns.columns,r):
            fdict['yyyy_mm_dd'].append(today)
            fdict['Symbol'].append(row[0])
            fdict['Share'].append(row[1][0][0:4])
        final_df = pd.DataFrame.from_dict(fdict)
        final_df = pd.merge(final_df,securities,on='Symbol')[['yyyy_mm_dd','Symbol',\
                                'Share','Close','Close3m','Close1m','Name','Sector']].reset_index(drop=True)
        final_df.to_csv('results/{}_{}.csv'.format(sector.lower().replace(' ','_'),today),index=False)
        print("Done producing optimal portfolio")
    except ValueError as error:
        print("Couldn't get Sharpe ratios - {}".format(error))

def update(sector,maxPrice):
    print(f"*****> Getting data for: {sector} <*****")
    securities = pd.read_csv('temp_data/sp500.csv')
    securities = securities[securities['Sector']==sector]
    securities = trim_too_expensive(securities,maxPrice)
    gen_portolio(securities,10000000,sector)


#trim the data
securities = pd.read_csv('temp_data/sp500.csv')
securities = securities[securities['Sector']=='Energy']
prices = close_prices_loop('3m',securities['Symbol'])['Close']
# prices['Date'] = prices.index
# prices.reset_index(drop=True,inplace=True)
print(prices.columns)
for col in prices.columns:
    if(prices[col].iloc[-1] > 100):
        prices.drop(col,inplace=True,axis=1)
print(prices.columns)

#get log returns
log_ret = pd.DataFrame(prices/prices.shift(1)-1)
# log_ret = pd.DataFrame(np.log(df/df.shift(1)))
# log_ret['Date'] = log_ret.index
# log_ret.reset_index(drop=True,inplace=True)
log_ret.fillna(0,inplace=True)
print(log_ret.head())

#sharpe ratios
today = datetime.datetime.strftime(datetime.datetime.today(),'%Y-%m-%d')
fdict = {'yyyy_mm_dd':[],'Symbol':[],'Share':[]}
final_df = pd.DataFrame()
cpp_ratios(log_ret,10000)
sol = open('temp_data/ratios.csv')
r = csv.reader(sol)
for row in zip(log_ret.columns,r):
    fdict['yyyy_mm_dd'].append(today)
    fdict['Symbol'].append(row[0])
    fdict['Share'].append(row[1][0][0:4])
final_df = pd.DataFrame.from_dict(fdict)
# need to pull the closes from 1 and 3 months ago
# final_df = pd.merge(final_df,securities,on='Symbol')[['yyyy_mm_dd','Symbol',\
                        # 'Share','Close','Close3m','Close1m','Name','Sector']].reset_index(drop=True)
# 'Energy' -> has to be replaced by Sector variable        
final_df.to_csv('results/{}_{}.csv'.format('Energy'.lower().replace(' ','_'),today),index=False)