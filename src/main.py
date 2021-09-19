# Personal stock portfolio creator WIP
# Author: Marc-Antoine Lacroix

import pandas as pd
import utils,sharpe
import ctypes
import os

def compile(libName,sourceFile):
    os.system("g++ --std=c++17 -shared -Wl,-install_name,{n}.so -o {n}.so -fPIC {s}.cpp "\
            "-I/Library/Frameworks/Python.framework/Versions/3.9/include/python3.9".format(n=libName,s=sourceFile))

def main():
    
    ###### cpp code
    # compile('cpp_sharpe','sharpe')
    # cpp_sharpe = ctypes.CDLL('cpp_sharpe.so')
    # dummy_returns = [100.0,0.01,0.01,23.0,0.10]
    # dummy_std = [0.1,10.0,10.0,1.01,0.04]
    # arr1 = (ctypes.c_float*len(dummy_returns))(*dummy_returns)
    # arr2 = (ctypes.c_float*len(dummy_std))(*dummy_std)
    # cpp_sharpe.someSum(arr1,arr2)

    ###### DEBUG ######
    # securities = utils.get_sp500()[0:200]
    # securities = utils.trim_too_expensive(securities,50) # 50 = arbitrary close price
    ###### DEBUG ######
    securities = pd.read_csv('temp_data/securities.csv')[0:20]
    print(securities)
    sharpe.print_portolio(securities,1,False) 


    
if __name__ == "__main__":
    main()