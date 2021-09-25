# Personal stock portfolio creator WIP
# Author: Marc-Antoine Lacroix

import pandas as pd
import utils,sharpe
import os

def main():
    
    securities = utils.get_sp500()
    securities = utils.trim_too_expensive(securities,30) # 50 = arbitrary close price
    sharpe.print_portolio(securities,10000000,False) 


    
if __name__ == "__main__":
    main()