# sk tmap 유료 api 설정.
# 무료 하루 100건.
import pandas as pd
import requests
import warnings
from tqdm import tqdm
import time
warnings.filterwarnings('ignore')

df = pd.read_csv("쉬영갑서.csv", encoding="cp949")
df['congestion'] = [0 for i in range(len(df))]
df['congestionLevel'] = [0 for i in range(len(df))]

slist= []
levellist=[]

for i in tqdm(range(len(df)), desc="Processing"):
    
    lon = df[['위도','경도']].iloc[i,:][1]
    #print(lon,lat)
    lat = df[['위도','경도']].iloc[i,:][0]
    
    url = "https://apis.openapi.sk.com/tmap/geo/reverseLabel"
    params = {
        'version': '1',
        'format': 'json',
        'callback': 'result',
        'reqLevel': '15',
        'centerLon': f'{lon}',
        'centerLat': f'{lat}',
        'reqCoordType': 'WGS84GEO',
        'resCoordType': 'WGS84GEO',
        'appKey': 'egFFUWxOY21RBraQKmcSgWA6xj8pBNu3aZ4uatE9'
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        result_json = response.json()
        #print(result_json['poiInfo']['id'])
    elif response.status_code == 429:
        print(f"Failed to retrieve data. Status code: {response.status_code}",i)
        break
    elif response.status_code == 403:
        print(f"Failed to retrieve data. Status code: {response.status_code}",i)
        break
    else:
        #print(f"not data. Status code1: {response.status_code}",i)
        slist.append('')
        levellist.append('')
        continue
        
    url = f"https://apis.openapi.sk.com/tmap/puzzle/pois/{result_json['poiInfo']['id']}"
    params = {
        'format': 'json',
        'appKey': 'egFFUWxOY21RBraQKmcSgWA6xj8pBNu3aZ4uatE9',
        'lat': f'{lat}',
        'lng': f'{lon}'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        result_json = response.json()
       
        slist.append(result_json['contents']['rltm'][0]['congestion'])
        levellist.append(result_json['contents']['rltm'][0]['congestionLevel'])
    elif response.status_code == 429:
        print(f"Failed to retrieve data. Status code2: {response.status_code}",i)
        break
    elif response.status_code == 403:
        print(f"Failed to retrieve data. Status code2: {response.status_code}",i)
        break
    else:
        slist.append('')
        levellist.append('')
        
for i in range(len(slist)):
    df['congestion'].iloc[i]=slist[i]
    df['congestionLevel'].iloc[i]=levellist[i]

df.to_csv("update_realtime.csv", index=False, encoding="cp949")