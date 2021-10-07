# Personal stock portfolio creator WIP
# Author: Marc-Antoine Lacroix

import utils
import pandas as pd
import portfolio_management as pm

def gen_all(stocks=100,max_price=100):
    sectors = list(pd.read_csv('temp_data/sp500.csv')['Sector'].unique())
    portfolios = []
    for sector in sectors:
        portfolios.append(pm.Portfolio(stocks,sector,max_price))
    for obj in portfolios:
        try:
            obj.trigger_update() 
        except ValueError as err:
            print(f"%%%%% Error generating portolio {err} %%%%%")

def main():
    
    utils.get_sp500()
    utils.compile('cpp_sharpe','sharpe')
    gen_all()
    
if __name__ == "__main__":
    main()