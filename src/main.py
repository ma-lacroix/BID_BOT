# Personal stock portfolio creator WIP
# Author: Marc-Antoine Lacroix

import utils

def main():
    
    securities = utils.get_sp500()
    securities = utils.trim_too_expensive(securities,100)
    utils.print_portolio(securities,1000000,False) 

if __name__ == "__main__":
    main()