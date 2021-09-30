# Personal stock portfolio creator WIP
# Author: Marc-Antoine Lacroix

import portfolio_management as pm

def main():
    
    healthcare = pm.Portfolio(100,'Health Care')
    healthcare.trigger_update()

if __name__ == "__main__":
    main()