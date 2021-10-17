import utils
import pandas as pd
import json
import time
import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

key = 'key/key.json'

def get_project():
# hide projectId
    with open(key) as f:
        projectId = json.load(f)['project_id']
        print(projectId)
    f.close()
    return projectId

def get_client():
    client = service_account.Credentials.from_service_account_file(key)
    return client

def read_csv(projectId,csv,client):
    df = pd.read_csv(csv)
    table = 'bid_bot.' + csv.replace('.csv','')\
                            .replace('results/','')\
                            .replace('-','')
    print(table)
    df.to_gbq(table,project_id=projectId,credentials=client,if_exists='replace')

def submit_job(query,clientq,config,projectId,counter):
    
    try:
        print("Trying query...")
        bigquery.QueryJobConfig
        query_job = clientq.query(query, job_config=config)  # Make an API request.
        query_job.result()  # Wait for the job to complete.
    except:
        counter+=1
        if(counter<6):
            print("Query failed; trying again...")
            time.sleep(5)
            submit_job(clientq,config,projectId,counter)
        else:
            return


def update_recent(projectId):
    clientq = bigquery.Client.from_service_account_json(key)
    config = bigquery.QueryJobConfig(destination=f'{projectId}.bid_bot.most_recent',
                                        write_disposition='WRITE_TRUNCATE')
    query = f'''
        WITH r AS (SELECT 
            MAX(yyyy_mm_dd) AS recent
            FROM `{projectId}.bid_bot.*`
        ), data AS (
            SELECT
            *
            FROM `{projectId}.bid_bot.*`
            WHERE yyyy_mm_dd = (
                SELECT recent FROM r
                )
            AND REGEXP_CONTAINS(_TABLE_SUFFIX,r".*\_[0-9]{{8}}")
            GROUP BY 1,2,3,4,5,6,7,8,9,10
            )
            SELECT * FROM data WHERE Share > 0
    '''
    submit_job(query,clientq,config,projectId,0)

def get_stock_list(projectId,Sector,client):
    query = f'''
        SELECT 
            Symbol
        FROM `mythical-harbor-167208.bid_bot.most_recent`
        WHERE Symbol != 'TOTAL'
        AND Sector = '{Sector}'
        GROUP BY 1
    '''
    df = pd.read_gbq(query,projectId,credentials=client)
    return df

def trigger_upload(csv):
    print("Uploading to BigQuery")
    projectId = get_project()
    client = get_client()
    read_csv(projectId,csv,client)
    update_recent(projectId)

def get_performance(sector='Energy'):
    today = datetime.date.today().strftime('%Y%m%d')
    client = get_client()
    projectId = get_project()
    table = f'bid_bot.performance_{sector}_{today}'
    
    stocks = list(get_stock_list(projectId,sector,client)['Symbol'])
    df = utils.close_prices_loop('3m',stocks)['Close']
    df['yyyy_mm_dd'] = df.index
    df['yyyy_mm_dd'] = df['yyyy_mm_dd'].dt.strftime('%Y-%m-%d')
    df.to_gbq(table,project_id=projectId,credentials=client,if_exists='replace')