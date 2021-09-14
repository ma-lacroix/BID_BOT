# Personal stock portfolio creator WIP
# Author: Marc-Antoine Lacroix

import pandas as pd
import utils,sharpe
import ctypes
import os

def compile(libName,sourceFile):
    os.system("g++ --std=c++17 -shared -Wl,-install_name,{n}.so -o {n}.so -fPIC {s}.cpp"\
                                .format(n=libName,s=sourceFile))

def main():
    
    # cpp code
    compile('cpp_sharpe','sharpe')
    cpp_sharpe = ctypes.CDLL('cpp_sharpe.so')
    dummy_returns = [100.0,0.01,0.01,23.0,0.10]
    dummy_std = [0.1,10.0,10.0,1.01,0.04]
    cpp_sharpe.listTupleToVector_Int(dummy_returns)
    cpp_sharpe.listTupleToVector_Int(dummy_std)
    # sharpe_factors = cpp_sharpe.get_sharpe_ratios(10000000,dummy_returns,dummy_std)

    ###### DEBUG ######
    # securities = utils.get_sp500()[0:200]
    # securities = utils.trim_too_expensive(securities,50) # 50 = arbitrary close price
    # securities = pd.read_csv('temp_data/securities.csv')[0:20]
    # sharpe.print_portolio(securities,1,False) 
    ###### DEBUG ######

    
if __name__ == "__main__":
    main()