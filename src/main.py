# Personal stock portfolio creator WIP
# Author: Marc-Antoine Lacroix

import utils
import portfolio_management as pm

def main():
    
    utils.get_sp500()
    utils.compile('cpp_sharpe','sharpe')

    healthcare = pm.Portfolio(100,'Health Care',100)
    healthcare.trigger_update()

    energy = pm.Portfolio(100,'Energy',100)
    energy.trigger_update()

    utilities = pm.Portfolio(100,'Utilities',100)
    utilities.trigger_update()

    industrials = pm.Portfolio(100,'Industrials',100)
    industrials.trigger_update()

if __name__ == "__main__":
    main()