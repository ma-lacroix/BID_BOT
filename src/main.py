# Personal stock portfolio creator WIP
# Author: Marc-Antoine Lacroix

import utils
import sys
import pandas as pd
import portfolio_management as pm

def gen_all(stocks=50,max_price=100):
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
    
    try:
        stocks = sys.argv[1]
        max_price = sys.argv[2]
    except:
    # defaults
        stocks = 50
        max_price = 100
    
    gen_all(stocks,max_price)
    
if __name__ == "__main__":
#to run: main.py numStocks max_price
    main()