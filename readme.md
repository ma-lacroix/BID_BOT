# Bid Bot <WIP>

This repo contains code to output investment portfolio suggestions based off the Sharpe ratio maxima values. The programs' general flows goes as follows:

* The user inputs the max value of a stock's last closing price as well as the total number of stocks they want to own
* The application pulls the current list of the S&P500 index
* For each sector, 
    * Daily closing prices are pulled for a given timeframe
    * Avg daily returns and standard deviations are calculated for each stock
    * Portolios are randomly generated as well as their Sharpe values
    * The program returns the optimal portfolio allocation
    * The user can then use this information to purchase some stocks

## How to use

The user will need the following to run `main.py`:
* Python 3.6 or later
* A c++17 compatible compiler
* Access to a Google Cloud service account with BigQuery job rights

## Disclaimer

Use at your own risk. If you make money with this code, good for you! If not, too bad!