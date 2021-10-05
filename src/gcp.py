
import pandas as pd
import json
from google.oauth2 import service_account

def get_project():
# hide projectId
    with open('key/key.json') as f:
        projectId = json.load(f)['project_id']
        print(projectId)
    f.close()
    return projectId

def get_client():
    client = service_account.Credentials.from_service_account_file('key/key.json')
    return client

def read_csv(projectId,csv,client):
    df = pd.read_csv(csv)
    table = 'bid_bot.' + csv.replace('.csv','')\
                            .replace('results/','')\
                            .replace('portfolio_','')\
                            .replace('-','')
    print(table)
    df.to_gbq(table,project_id=projectId,credentials=client,if_exists='replace')

def trigger_upload(csv):
    projectId = get_project()
    client = get_client()
    read_csv(projectId,csv,client)