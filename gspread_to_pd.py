from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
import pandas as pd
import gspread
from os.path import expanduser
import yaml

with open(expanduser('~')+'/cred_config/.credential_config.ymlconfig.yml','r') as yaml_file:
    conf_data = yaml.load(yaml_file)
    doc_id = conf_data['gs_test']['doc_id'] 


scopes = ['https://www.googleapis.com/auth/spreadsheets']
json_file = expanduser('~') + '/cred_config/client_secret2.json'#OAuth用クライアントIDの作成でダウンロードしたjsonファイル
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scopes=scopes)
http_auth = credentials.authorize(Http())
# スプレッドシート用クライアントの準備
gc = gspread.authorize(credentials)
#wb = gc.open_by_url('https://docs.google.com/spreadsheets/d/xxx/edit#gid=0') #urlの場合 
wb = gc.open_by_key(doc_id)  #読み書きするgoogle spreadsheet

#worksheet = wb.worksheet("sheet1")
ws = wb.sheet1
#print(ws.cell(1,1).value)
#print(ws.get_all_values())


df = pd.DataFrame(ws.get_all_values())
header = df.iloc[0]
df.drop(0,axis=0,inplace=True)
df.rename(columns=header,inplace=True)
df.reset_index(drop=True,inplace=True)
print(df.head(6))