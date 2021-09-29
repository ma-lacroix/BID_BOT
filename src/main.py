# Personal stock portfolio creator WIP
# Author: Marc-Antoine Lacroix

import utils
import pandas as pd

def main():
    
    securities = utils.get_sp500()
    securities = securities[securities['Sector'].isin(['Health Care','Energy'])]
    securities = utils.trim_too_expensive(securities,100)
    utils.print_portolio(securities,100) 

if __name__ == "__main__":
    main()