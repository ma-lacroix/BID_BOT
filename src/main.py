# Personal stock portfolio creator WIP
# Author: Marc-Antoine Lacroix

import pandas as pd
import utils,sharpe

def main():
    
    securities = utils.get_sp500()
    securities = utils.trim_too_expensive(securities,50) # 50 = arbitrary close price
    sharpe.print_portolio(securities,100,False) # 100 simulations too low
    
if __name__ == "__main__":
    main()