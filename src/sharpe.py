# Using the Sharpe ratio, the 

import datetime
import pandas as pd
import numpy as np
from pandas_datareader import data as dr
import utils
import csv
import os
from os import path
import ctypes

def compile(libName,sourceFile):
    os.system("g++ --std=c++17 -shared -Wl,-install_name,{n}.so -o {n}.so -fPIC {s}.cpp "\
            "-I/Library/Frameworks/Python.framework/Versions/3.9/include/python3.9".format(n=libName,s=sourceFile))

def cpp_ratios(df):
    compile('src/cpp_sharpe','src/sharpe')
    cpp_sharpe = ctypes.CDLL('src/cpp_sharpe.so')
    dummy_returns = list(df.mean()*len(df))
    dummy_std = list(df.std()*len(df))
    arr_size = (ctypes.c_int)
    arr_size = len(dummy_std)
    arr1 = (ctypes.c_float*len(dummy_returns))(*dummy_returns)
    arr2 = (ctypes.c_float*len(dummy_std))(*dummy_std)
    cpp_sharpe.showSharpe(arr1,arr2,arr_size)

def get_sharp_ratio(simulations,df):
# to be rewritten in C++ to handle much higher number of simulations
    print("\nGetting Sharpe ratios...\n")
    all_weights = np.zeros((simulations,len(df.columns)))
    ret_arr = np.zeros(simulations)
    vol_arr = np.zeros(simulations)
    sharpe_arr = np.zeros(simulations)

    for ind in range(simulations):
        weights = np.array(np.random.random(len(df.columns)))
        weights = weights / np.sum(weights)
        all_weights[ind,:] = weights
        ret_arr[ind] = np.sum((df.mean() * weights) *len(df))
        # vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(df.cov() * len(df), weights)))
        vol_arr[ind] = np.dot(df.std()*len(df), weights)
        sharpe_arr[ind] = ret_arr[ind]/vol_arr[ind]
    return np.round(all_weights[sharpe_arr.argmax(),:],3)

def print_portolio(securities,simulations,grouping):
    print("\nToday's date: {}\r".format(datetime.date.today()))
    try:
        
        ###### DEBUG ######
        # log_returns = utils.get_log_ret('1m',securities['Symbol'])
        log_returns = pd.read_csv('temp_data/returns.csv',index_col='Date')
        ###### DEBUG ######

        if(grouping):
            log_returns.columns=securities['Sector']
            log_returns = log_returns.groupby(log_returns.columns, axis=1).sum()
        # sol = get_sharp_ratio(simulations,log_returns)
        cpp_ratios(log_returns)
        print("Optimal portfolio allocation (based on last month): ")
        sol = open('temp_data/ratios.csv')
        r = csv.reader(sol)
        for row in zip(log_returns.columns,r):
            print(row[0],row[1])
    except ValueError as error:
        print("Couldn't get Sharpe ratios - {}".format(error))
