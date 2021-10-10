
import pandas as pd
import json
import time
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

def submit_job(client,config,projectId):
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
  GROUP BY 1,2,3,4,5,6,7,8,9,10
  )
SELECT * FROM data WHERE Share > 0
    '''
    try:
        print("Trying query...")
        bigquery.QueryJobConfig
        query_job = client.query(query, job_config=config)  # Make an API request.
        query_job.result()  # Wait for the job to complete.
    except:
        print("Query failed; trying again...")
        time.sleep(5)
        submit_job(client,config,projectId)


def update_recent(projectId):
    client = bigquery.Client.from_service_account_json(key)
    config = bigquery.QueryJobConfig(destination=f'{projectId}.bid_bot.most_recent',
                                        write_disposition='WRITE_TRUNCATE')
    submit_job(client,config,projectId)


def trigger_upload(csv):
    projectId = get_project()
    client = get_client()
    read_csv(projectId,csv,client)
    update_recent(projectId)
