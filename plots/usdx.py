import pandas as pd 
import numpy as np
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

# plot
fig = plt.subplots(figsize=(10, 6))
usdx['fed USD idx'].plot(color='blue', linestyle='--', label='fed USD index')
usdx['DXY'].plot(color='black', label='DXY (yfinance)')
usdx['manual DXY'].plot(color='red', linestyle='--', label='manually-computed DXY')
plt.ylabel('USD index')
plt.xlabel('date')
plt.legend()
plt.title('comparison of USD indices')
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usdx-comparison.png')

# compare for validation
plt.figure(figsize=(6,6))
x = usdx['manual DXY']
y = usdx['DXY']
plt.scatter(x, y, s=5)
lims = [min(x.min(), y.min()), max(x.max(), y.max())]
plt.plot(lims, lims, '--', color='gray')
plt.xlabel("manual DXY")
plt.ylabel("DXY")
plt.title("manually-computed DXY vs Yahoo Finance DXY")
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/dxy-validation.png')
plt.show()

diff = usdx['DXY'] - usdx['manual DXY']
mae  = np.mean(np.abs(diff))
rmse = np.sqrt(np.mean(diff**2))
mape = np.mean(np.abs(diff / usdx['DXY'])) * 100

print(f"MAE:  {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"MAPE: {mape:.2f}%")