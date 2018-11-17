import pandas as pd
import requests
from pandas.io.json import json_normalize
from datetime import datetime
import time
from urllib.parse import unquote
from pathlib import Path


class Td:
    def __init__(self, refresh_token, client_id, apikey):
        # URL decoded refresh token
        self.refresh_token = unquote(refresh_token)
        self.code = unquote(refresh_token)
        self.apikey = apikey
        self.client_id = client_id
        self.main()


    # Checks if token file is available
    # token file : refresh-token.txt
    #
    def main(self):
        refresh_token_file = Path("refresh-token.txt")
        if refresh_token_file.is_file():
            self.get_access_token()
        else:
            self.auth_code()

    # Save a refresh token
    # token file : refresh-token.txt
    #
    def auth_code(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'access_type': 'offline',
            'code': self.code,
            'client_id': self.client_id,
            'redirect_uri': 'http://localhost:8080'
        }
        authReply = requests.post(
            'https://api.tdameritrade.com/v1/oauth2/token',
            headers=headers,
            data=data)
        if authReply.status_code == 200:
            refresh_token = authReply.json()
            f = open("refresh-token.txt", "w+")
            f.write(refresh_token['refresh_token'])
            f.close()
        else:
            print('Failed to obtain a refresh token: auth_code(): Status',
                  authReply.status_code)
            print('Obtain a new Code from TDAmeritrade')


    # Gets Access Token
    #
    #
    def get_access_token(self):
        #Post Access Token Request
        my_file = Path("refresh-token.txt")
        if my_file.is_file():
            f = open("refresh-token.txt", "r")
            if f.mode == 'r':
                token = f.read()
                f.close()
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                data = {
                    'grant_type': 'refresh_token',
                    'refresh_token': token,
                    'access_type': 'offline',
                    'client_id': self.client_id,
                    'redirect_uri': 'http://localhost:8080'
                }
                authReply = requests.post(
                    'https://api.tdameritrade.com/v1/oauth2/token',
                    headers=headers,
                    data=data)
                if authReply.status_code == 200:
                    refresh_token = authReply.json()
                    f = open("refresh-token.txt", "w+")
                    f.write(refresh_token['refresh_token'])
                    f.close()
                else:
                    print(authReply.json())
        return authReply


    # Get Qoute
    # Param : Symbol
    #
    def get_quotes(self, symbol):
        access_token = self.get_access_token().json()
        access_token = access_token['access_token']
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer {}'.format(access_token)
        }
        data = {'symbol': symbol, 'apikey': self.apikey}
        authReply = requests.get(
            'https://api.tdameritrade.com/v1/marketdata/quotes',
            headers=headers,
            params=data)
        return (authReply.json())


    # Convert time to Unix Time Stamp
    # Param : Time
    #
    def unix_time_millis(self, dt):
        epoch = datetime.utcfromtimestamp(0)
        return int((dt - epoch).total_seconds() * 1000.0)


    # Get price History
    # Param : Symbol, Start date , End date
    #
    def get_price_history(self, symbol, startDate=None, endDate=None):
        access_token = self.get_access_token().json()
        access_token = access_token['access_token']
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer {}'.format(access_token)
        }
        data = {
            'periodType': 'year',
            'frequencyType': 'daily',
            'startDate': startDate,
            'endDate': endDate
        }
        authReply = requests.get(
            'https://api.tdameritrade.com/v1/marketdata/' + symbol +
            '/pricehistory',
            headers=headers,
            params=data)
        candles = authReply.json()
        df = json_normalize(authReply.json())
        df = pd.DataFrame(candles['candles'])
        return df


code=''
apikey ='xxxxxx@AMER.OAUTHAP'
client_id = 'xxxxxxx@AMER.OAUTHAP'

p = Td(code, client_id, apikey)

start_date = datetime.strptime('04 3 2018  1:33PM', '%m %d %Y %I:%M%p')
end_date = datetime.strptime('05 3 2018  1:33PM', '%m %d %Y %I:%M%p')
print(p.get_price_history('SNAP', p.unix_time_millis(start_date),
                          p.unix_time_millis(end_date)))
