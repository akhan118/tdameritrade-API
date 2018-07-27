import pandas as pd
import requests
from pandas.io.json import json_normalize
from datetime import datetime
import time

class Td:
    def __init__(self,refresh_token,client_id,apikey):
        # URL decoded refresh token
        self.refresh_token= refresh_token
        self.apikey= apikey
        self.client_id= client_id

    def get_access_token(self):
        #Post Access Token Request
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        data = { 'grant_type': 'refresh_token',  'refresh_token': self.refresh_token,
        'client_id': self.client_id, 'redirect_uri': 'http://localhost:8080'}
        authReply = requests.post('https://api.tdameritrade.com/v1/oauth2/token', headers=headers, data=data)
        return authReply
        # print(results['access_token'])

    def get_quotes(self,symbol):
        access_token = self.get_access_token().json()
        access_token = access_token['access_token']
        headers={'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(access_token)}
        data = { 'symbol': symbol,  'apikey': self.apikey}
        authReply = requests.get('https://api.tdameritrade.com/v1/marketdata/quotes',
        headers=headers, params=data)
        # print(authReply)
        return (authReply.json())


    def unix_time_millis(self,dt):
        epoch = datetime.utcfromtimestamp(0)
        return int((dt - epoch).total_seconds() * 1000.0)

    def get_price_history(self,symbol,startDate=None,endDate=None):
        access_token = self.get_access_token().json()
        access_token = access_token['access_token']
        headers={'Content-Type': 'application/x-www-form-urlencoded',
         'Authorization': 'Bearer {}'.format(access_token)}
        data = { 'periodType': 'year','frequencyType':'daily',
        'startDate':startDate,'endDate':endDate}
        authReply = requests.get('https://api.tdameritrade.com/v1/marketdata/'+symbol+'/pricehistory',
        headers=headers, params=data)
        # print(authReply.json())
        candles = authReply.json()
        df = json_normalize(authReply.json())
        df = pd.DataFrame(candles['candles'])
        return df



token=''
apikey ='xxxxxx@AMER.OAUTHAP'
client_id = 'xxxxxxx@AMER.OAUTHAP'

p = Td(token,client_id,apikey)
start_date = datetime.strptime('04 3 2018  1:33PM', '%m %d %Y %I:%M%p')
end_date = datetime.strptime('05 3 2018  1:33PM', '%m %d %Y %I:%M%p')
print(p.get_price_history('SNAP',p.unix_time_millis(start_date),p.unix_time_millis(end_date)))
