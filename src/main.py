# Personal stock portfolio creator WIP
# Author: Marc-Antoine Lacroix

import pandas as pd
import utils,sharpe

def main():
    
    ##### DEBUG #####
    # securities = utils.get_sp500()
    securities = pd.read_csv('temp_data/sp500.csv').iloc[0:50]
    ##### END DEBUG #####
    
    securities = utils.trim_too_expensive(securities,50)
    # sharpe.print_portolio(securities,100,False)
    
if __name__ == "__main__":
    main()