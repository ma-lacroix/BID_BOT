# Using the Sharpe ratio, the 

import datetime
import pandas as pd
import numpy as np
from pandas_datareader import data as dr
import utils
import os
from os import path

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
        vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(df.cov() * len(df), weights)))
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
        sol = get_sharp_ratio(simulations,log_returns)
        print("Optimal portfolio allocation (based on last month): ")
        for row in zip(log_returns.columns,sol):
            print(row[0],': ',row[1])
    except ValueError as error:
        print("Couldn't get Sharpe ratios - {}".format(error))
