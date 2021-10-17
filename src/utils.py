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

def close_prices_loop(security):
# minimizes the number of simultaneous stock price GET requests 
    print("Getting closing prices...")
    df = pd.DataFrame()
    num = len(security)
    residue = num%5
    incr = int((num-residue)/5)
    cnt = 0
    while(cnt<num-residue):
        df2 = get_close_prices(security[cnt:cnt+incr])
        df = pd.concat([df2,df],axis=1)
        time.sleep(2.0) # adding small buffer
        cnt+=incr
    if(residue>0):
        df2 = get_close_prices(security[cnt:cnt+residue+1])
        time.sleep(2.0) # adding small buffer
        df = pd.concat([df2,df],axis=1)
    df.fillna(0,inplace=True)
    return df

def get_close_prices(security):    
    service = 'yahoo'
    start = (datetime.datetime.today()-datetime.timedelta(days=93)).strftime('%Y-%m-%d')
    end = datetime.datetime.today().strftime('%Y-%m-%d')        
    try:
        df = np.round(dr.DataReader(security,service,start,end),2)
        # df.sort_values('Date',inplace = True)
    except RemoteDataError:
        print("Data not found at Ticker {}".format(security))
    return df

def get_log_ret(prices):
    #get log returns
    log_ret = pd.DataFrame(prices/prices.shift(1)-1)
    # log_ret = pd.DataFrame(np.log(df/df.shift(1)))
    # log_ret['Date'] = log_ret.index
    # log_ret.reset_index(drop=True,inplace=True)
    log_ret.fillna(0,inplace=True)
    log_ret.to_csv('temp_data/returns.csv')
    return log_ret

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

def gen_portolio(securities,prices,simulations,sector):
    today = datetime.datetime.strftime(datetime.datetime.today(),'%Y-%m-%d')
    fdict = {'yyyy_mm_dd':[],'Symbol':[],'Share':[]}
    log_ret = get_log_ret(prices)
    final_df = pd.DataFrame()
    cpp_ratios(log_ret,simulations)
    sol = open('temp_data/ratios.csv')
    r = csv.reader(sol)
    for row in zip(log_ret.columns,r):
        fdict['yyyy_mm_dd'].append(today)
        fdict['Symbol'].append(row[0])
        fdict['Share'].append(row[1][0][0:4])
    final_df = pd.DataFrame.from_dict(fdict)
    final_df = pd.merge(final_df,securities,on='Symbol')[['yyyy_mm_dd','Symbol',\
                            'Share','Close','Close3m','Close1m','Name','Sector']].reset_index(drop=True)
    final_df.to_csv('results/{}_{}.csv'.format(sector.lower().replace(' ','_'),today),index=False)

def genData(securities,maxPrice):
    prices = close_prices_loop(securities['Symbol'])['Close']
    for col in prices.columns:
        if(prices[col].iloc[-1] > maxPrice):
            prices.drop(col,inplace=True,axis=1)
    prices1d = prices.iloc[-1].reset_index() # not exactly 1 month
    prices1d.columns = ['Symbol','Close']
    prices1m = prices.iloc[-25].reset_index() # not exactly 1 month
    prices1m.columns = ['Symbol','Close1m']
    prices3m = prices.iloc[0].reset_index()
    prices3m.columns = ['Symbol','Close3m']
    pList = [prices,prices1d,prices1m,prices3m]
    return pList

def mergeSecPrices(pList,securities):
    for p in pList:
        securities = pd.merge(securities,p,on='Symbol')
    return securities

def update(sector,maxPrice):
    print(f"*****> Getting data for: {sector} <*****")
    securities = pd.read_csv('temp_data/sp500.csv')
    securities = securities[securities['Sector']==sector]
    pList = genData(securities,maxPrice)
    securities = mergeSecPrices(pList[1:4],securities)
    gen_portolio(securities,pList[0],10000000,sector)

