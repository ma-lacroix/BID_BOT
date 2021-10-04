# graphing tools to help manage 

import pandas as pd
import numpy as np
import os
import utils
import gcp

class Portfolio:

    def __init__(self,stocks,sector,maxPrice):
        self.csv_file = ""
        self.stocks = stocks
        self.sector = sector
        self.maxPrice = maxPrice
        self.df = pd.DataFrame()

    def init_csv_file(self):
        last_file = max([f for f in os.listdir('results/') if self.sector.lower().replace(' ','_') in f])
        self.csv_file = 'results/'+last_file

    def init_df(self):
        self.df = pd.read_csv(self.csv_file)
        self.df = self.df[self.df['Sector']==self.sector][['Symbol','Share','Close','Name']]\
            .sort_values(by='Share',ascending=False).reset_index(drop=True)
    
    def get_shares(self):
        total_price = []
        total_stocks = []
        for index,row in self.df.iterrows():
            check = (self.stocks*row['Share'])
            if(check > 0):
                total_price.append(check*row['Close'])
                total_stocks.append(check)
            else:
                total_price.append(0)
                total_stocks.append(0)
        self.df['total_price'] = np.round(total_price,2)
        self.df['total_stocks'] = np.round(total_stocks,0)
        self.df.to_csv(self.csv_file,index=False) # overwrite results file            
        print(self.df)

    def cash_needed(self):
        print(np.round(np.sum(self.df.total_price),2))

    def trigger_update(self):
        utils.update(self.sector,self.maxPrice)
        self.init_csv_file()
        self.init_df()
        self.get_shares()
        self.cash_needed()
        gcp.trigger_upload(self.csv_file)
        
