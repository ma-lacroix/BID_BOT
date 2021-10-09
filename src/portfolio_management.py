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
        self.df = self.df[['yyyy_mm_dd','Symbol','Share','Name','Close','Close3m','Close1m']]\
            .sort_values(by='Share',ascending=False).reset_index(drop=True)
    
    def get_shares(self):
        total_price = []
        total_stocks = []
        gains_6m = []
        gains_3m = []
        gains_1m = []
        for index,row in self.df.iterrows():
            check = (self.stocks*row['Share'])
            if(check > 0):
                total_price.append(check*row['Close'])
                total_stocks.append(check)
                gains_3m.append(check*row['Close']-check*row['Close3m'])
                gains_1m.append(check*row['Close']-check*row['Close1m'])
            else:
                total_price.append(0)
                total_stocks.append(0)
                gains_6m.append(0)
                gains_3m.append(0)
                gains_1m.append(0)
        self.df['Sector'] = self.sector
        self.df['total_price'] = np.round(total_price,2)
        self.df['total_stocks'] = np.round(total_stocks,0)
        self.df['exp_gains_3m'] = np.round(gains_3m,2)
        self.df['exp_gains_1m'] = np.round(gains_1m,2)
        totals = {'Sector':self.sector,'yyyy_mm_dd':self.df['yyyy_mm_dd'][0],'Symbol':'TOTAL'.format(self.sector),
                    'Share':1.0,'Close':np.sum(self.df['Close']),'Close3m':np.sum(self.df['Close']),
                    'Name':'TOTAL','total_price':np.sum(self.df['total_price']),
                    'total_stocks':np.sum(self.df['total_stocks']),'exp_gains_3m':np.sum(self.df['exp_gains_3m']),
                    'exp_gains_1m':np.sum(self.df['exp_gains_1m'])}
        self.df = self.df.append(totals,ignore_index=True)[['Sector','yyyy_mm_dd','Symbol','Name','Share','Close','total_price',
                                                            'total_stocks','exp_gains_3m','exp_gains_1m']]
        self.df.to_csv(self.csv_file,index=False) # overwrite results file            
        print(self.df)

    def trigger_update(self):
        # utils.update(self.sector,self.maxPrice)
        self.init_csv_file()
        # self.init_df()
        # self.get_shares()
        gcp.trigger_upload(self.csv_file)
        
