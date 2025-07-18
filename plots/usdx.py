import pandas as pd 
import matplotlib.pyplot as plt

# fed nominal broad US dollar index
from fredconnect import fred

fed_nominal_broad_usd_idx = pd.DataFrame(fred.get_series('DTWEXBGS'))
fed_nominal_broad_usd_idx.index = pd.to_datetime(fed_nominal_broad_usd_idx.index).tz_localize(None)

# DXY
import yfinance as yf 
from curl_cffi import requests 

dxy = yf.Ticker("DX-Y.NYB", session=requests.Session(impersonate="chrome")).history(period="max")
dxy.index = pd.to_datetime(dxy.index).tz_localize(None)

# manual DXY calculation 
from loader import dxy_spots

c = 50.14348112

weights = {
    'EUR/USD': -0.576,
    'USD/JPY': 0.136,
    'GBP/USD': -0.119,
    'USD/CAD': 0.091,
    'USD/SEK': 0.042,
    'USD/CHF': 0.036
}

dxy_spots['DXY'] = c * (dxy_spots['EUR/USD'] ** weights['EUR/USD']) * \
    (dxy_spots['USD/YEN'] ** weights['USD/JPY']) * \
    (dxy_spots['GBP/USD'] ** weights['GBP/USD']) * \
    (dxy_spots['USD/CAD'] ** weights['USD/CAD']) * \
    (dxy_spots['USD/SEK'] ** weights['USD/SEK']) * \
    (dxy_spots['USD/CHF'] ** weights['USD/CHF'])

# combine
usdx = pd.concat([fed_nominal_broad_usd_idx, dxy['Close']], axis=1)
usdx.columns = ['fed USD idx', 'DXY']
usdx['manual DXY'] = dxy_spots['DXY']
usdx.dropna(inplace=True)
print(usdx)
