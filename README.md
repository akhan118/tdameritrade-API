# kiki
A Python Client For TdAmeritrade API


[Documentation](http://inside.probability.ninja/kiki-a-python-client-for-tdameritrade-api/) version 1.0.0


```python

Code=''
apikey ='xxxxxx@AMER.OAUTHAP'
client_id = 'xxxxxxx@AMER.OAUTHAP'

p = Td(code,client_id,apikey)
start_date = datetime.strptime('04 3 2018  1:33PM', '%m %d %Y %I:%M%p')
end_date = datetime.strptime('05 3 2018  1:33PM', '%m %d %Y %I:%M%p')

print(p.get_price_history('SNAP',p.unix_time_millis(start_date),
                                 p.unix_time_millis(end_date)))
```

```text
    close       datetime     high     low   open     volume
0   14.08  1522731600000  14.9000  13.800  14.80   33231754
1   14.59  1522818000000  14.7800  13.620  13.69   20131765
2   14.39  1522904400000  14.9600  14.195  14.70   17015408
3   14.25  1522990800000  14.5700  13.980  14.35   13533877
4   14.15  1523250000000  14.4700  14.040  14.28   12383904
5   14.48  1523336400000  14.5800  14.180  14.29   16351816
```
