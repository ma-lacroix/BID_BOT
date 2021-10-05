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
        self.df = self.df[['yyyy_mm_dd','Symbol','Share','Close','Name']]\
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
        totals = {'yyyy_mm_dd':self.df['yyyy_mm_dd'][0],'Symbol':'TOTAL','Share':1.0,'Close':np.sum(self.df['Close']),
                    'Name':'TOTAL','total_price':np.sum(self.df['total_price']),
                    'total_stocks':np.sum(self.df['total_stocks'])}
        self.df = self.df.append(totals,ignore_index=True)
        self.df.to_csv(self.csv_file,index=False) # overwrite results file            
        print(self.df)

    def trigger_update(self):
        utils.update(self.sector,self.maxPrice)
        self.init_csv_file()
        self.init_df()
        self.get_shares()
        gcp.trigger_upload(self.csv_file)
        
