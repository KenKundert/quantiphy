#!/usr/bin/env python3

# Bitcoin
# This example demonstrates how to use UnitConversion to convert between bitcoin
# and dollars at the current price.

from quantiphy import Quantity, UnitConversion
import requests

# get the current bitcoin price from coingecko.com
url = 'https://api.coingecko.com/api/v3/simple/price'
params = dict(ids='bitcoin', vs_currencies='usd')
def get_btc_price():
    try:
        resp = requests.get(url=url, params=params)
        prices = resp.json()
        return prices['bitcoin']['usd']
    except Exception as e:
        print('error: cannot connect to coingecko.com.')

# use UnitConversion from QuantiPhy to perform the conversion
# here we define the conversions, which then become available in calculator
bitcoin_units = ['BTC', 'btc', 'Ƀ', '₿']
satoshi_units = ['sat', 'sats', 'ș']
dollar_units = ['USD', 'usd', '$']
UnitConversion(
    dollar_units, bitcoin_units,
    lambda b: b*get_btc_price(), lambda d: d/get_btc_price()
)
UnitConversion(satoshi_units, bitcoin_units, 1e8)
UnitConversion(
    dollar_units, satoshi_units,
    lambda s: s*get_btc_price()/1e8, lambda d: d/(get_btc_price()/1e8),
)

unit_btc = Quantity('1 BTC')
unit_dollar = Quantity('$1')

print(f'{unit_btc:>8,.2p} = {unit_btc:,.2p$}')
print(f'{unit_dollar:>8,.2p} = {unit_dollar:,.0psat}')
