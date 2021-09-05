# Personal stock portfolio creator WIP
# Author: Marc-Antoine Lacroix

import pandas as pd
import utils,sharpe

def main():
    ###### DEBUG ######
    # securities = utils.get_sp500()[0:250]
    # securities = utils.trim_too_expensive(securities,50) # 50 = arbitrary close price
    ###### DEBUG ######
    securities = pd.read_csv('temp_data/securities.csv')
    sharpe.print_portolio(securities,3,False) # 100 simulations too low
    
if __name__ == "__main__":
    main()