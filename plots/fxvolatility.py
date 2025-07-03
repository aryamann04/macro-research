import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

euro_spot = pd.read_csv('/Users/aryaman/macro-research/data/eur-spot-daily.csv', index_col=0, parse_dates=True)
gbp_spot = pd.read_csv('/Users/aryaman/macro-research/data/gbp-spot-daily.csv', index_col=0, parse_dates=True)
yen_spot = pd.read_csv('/Users/aryaman/macro-research/data/yen-spot-daily.csv', index_col=0, parse_dates=True)
yuan_spot = pd.read_csv('/Users/aryaman/macro-research/data/yuan-spot-daily.csv', index_col=0, parse_dates=True)

spots = pd.DataFrame()
spots['EUR/USD'] = euro_spot['DEXUSEU']
spots['GBP/USD'] = gbp_spot['DEXUSUK']
spots['USD/YEN'] = yen_spot['DEXJPUS']
spots['USD/YUAN'] = yuan_spot['DEXCHUS']

spots = np.log(spots).diff().dropna()
# vol by year 

fxvol_by_year = spots.groupby(spots.index.year).std().mul(np.sqrt(252)).mul(100)
fxvol_by_year.index = pd.to_datetime(fxvol_by_year.index.astype(str) + '-12-31')

plt.figure(figsize=(10, 5))
fxvol_by_year['EUR/USD'].plot(label='EUR/USD', color='blue')
fxvol_by_year['GBP/USD'].plot(label='GBP/USD', color='green')
fxvol_by_year['USD/YEN'].plot(label='USD/YEN', color='red')
fxvol_by_year['USD/YUAN'].plot(label='USD/YUAN', color='orange')
        
plt.xlabel('year')
plt.ylabel('annualized volatility (%)')
plt.title(f'fx volatility by year')
plt.legend()
plt.tight_layout()
# plt.savefig('/Users/aryaman/macro-research/plots/figures/fxvolatility-by-year.png')

# vol by month 

fxvol_by_month = spots.resample('M').std().mul(np.sqrt(252)).mul(100)
# fxvol_by_month = fxvol_by_month.truncate(before='2023-01-01')

plt.figure(figsize=(10, 5))
fxvol_by_month['EUR/USD'].plot(label='EUR/USD', color='blue')
fxvol_by_month['GBP/USD'].plot(label='GBP/USD', color='green')
fxvol_by_month['USD/YEN'].plot(label='USD/YEN', color='red')
fxvol_by_month['USD/YUAN'].plot(label='USD/YUAN', color='orange')

plt.axvline(pd.to_datetime('2025-01-01'), color='black', linestyle='--', linewidth=1)
plt.axvline(pd.to_datetime('2025-06-01'), color='black', linestyle='--', linewidth=1)
plt.axvspan(pd.to_datetime('2025-01-01'), pd.to_datetime('2025-06-01'), color='gray', alpha=0.2)

plt.xlabel('month')
plt.ylabel('annualized volatility (%)')
plt.title(f'fx volatility by month')
plt.legend()
plt.tight_layout()
# plt.savefig('/Users/aryaman/macro-research/plots/figures/fxvolatility-by-month-full.png')

