import requests
import json

def getBTCExchangeRate(start, end, cache=None):
    if start is 'BTC':
        direction = 'sell'
        curr = end
    elif end is 'BTC':
        direction = 'buy'
        curr = start
    else:
        raise ValueError('Either start or end currency has to be BTC')

    try:
        req = requests.get('https://blockchain.info/ticker')
        rates = req.json()
        return rates[curr][direction]
    except json.JSONDecodeError:
        if cache:
            return cache.get('exchange_rates', 60*60)
        else:
            return False
