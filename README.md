# kiki
A Python Client For TdAmeritrade API


token=''
apikey ='xxxxxx@AMER.OAUTHAP'
client_id = 'xxxxxxx@AMER.OAUTHAP'

p = Td(token,client_id,apikey)
start_date = datetime.strptime('04 3 2018  1:33PM', '%m %d %Y %I:%M%p')
end_date = datetime.strptime('05 3 2018  1:33PM', '%m %d %Y %I:%M%p')
print(p.get_price_history('SNAP',p.unix_time_millis(start_date),p.unix_time_millis(end_date)))
