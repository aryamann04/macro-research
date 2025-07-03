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

# log returns 
spots = np.log(spots).diff().dropna()

# vol by year 
fxvol_by_year = spots.groupby(spots.index.year).std().mul(np.sqrt(252))
fxvol_by_year.index = pd.to_datetime(fxvol_by_year.index.astype(str) + '-12-31')
print(fxvol_by_year)
plt.figure(figsize=(10, 5))
fxvol_by_year['EUR/USD'].plot(marker='o', label='EUR/USD', color='blue')
fxvol_by_year['GBP/USD'].plot(marker='o', label='GBP/USD', color='green')
fxvol_by_year['USD/YEN'].plot(marker='o', label='USD/YEN', color='red')
fxvol_by_year['USD/YUAN'].plot(marker='o', label='USD/YUAN', color='orange')
        
plt.xlabel('year')
plt.ylabel('annualized volatility')
plt.title('annualized fx volatility by year')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/fxvolatility-by-year.png')

# vol by month 

fxvol_by_month = spots.resample('M').std().mul(np.sqrt(252))

plt.figure(figsize=(10, 5))
fxvol_by_month['EUR/USD'].plot(label='EUR/USD', color='blue')
fxvol_by_month['GBP/USD'].plot(label='GBP/USD', color='green')
fxvol_by_month['USD/YEN'].plot(label='USD/YEN', color='red')
fxvol_by_month['USD/YUAN'].plot(label='USD/YUAN', color='orange')

plt.axvline(pd.to_datetime('2025-01-01'), color='black', linestyle='--', linewidth=1)
plt.axvline(pd.to_datetime('2025-06-01'), color='black', linestyle='--', linewidth=1)
plt.axvspan(pd.to_datetime('2025-01-01'), pd.to_datetime('2025-06-01'), color='gray', alpha=0.2)

plt.xlabel('month')
plt.ylabel('annualized volatility')
plt.title('annualized fx volatility by month')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/fxvolatility-by-month.png')

# aggregate volatility - yearly 

agg_yearly_vol = fxvol_by_year.mean(axis=1)

plt.figure(figsize=(10, 5))
agg_yearly_vol.plot(marker='o')
plt.title('average (across 4 currency pairs) annualized fx volatility by year')
plt.ylabel('annualized volatility')
plt.xlabel('year')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/aggregate-fxvolatility-by-year.png')

# aggregate volatility - monthly 

agg_monthly_vol = fxvol_by_month.mean(axis=1)

plt.figure(figsize=(10, 5))
agg_monthly_vol.plot(marker='o')
plt.title('average (across 4 currency pairs) annualized fx volatility by month')
plt.ylabel('annualized volatility')
plt.xlabel('month')
plt.axvline(pd.to_datetime('2025-01-01'), color='black', linestyle='--', linewidth=1)
plt.axvline(pd.to_datetime('2025-06-01'), color='black', linestyle='--', linewidth=1)
plt.axvspan(pd.to_datetime('2025-01-01'), pd.to_datetime('2025-06-01'), color='gray', alpha=0.2)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/aggregate-fxvolatility-by-month.png')

# aggregate volatility - rolling windows 

plt.figure(figsize=(10, 5))

rolling_vol = pd.DataFrame(index=spots.index)

windows = [50, 100, 250]
for w in windows:
    rolling_vol[f'{w}'] = spots.rolling(window=w).std().mean(axis=1).mul(np.sqrt(252))
rolling_vol = rolling_vol.dropna()

rolling_vol['50'].plot(color='blue', label='50-day rolling volatility')
rolling_vol['100'].plot(color='green', label='100-day rolling volatility')
rolling_vol['250'].plot(color='red', label='250-day rolling volatility')

plt.title('rolling annualized fx volatility (average across 4 currency pairs)')
plt.ylabel('annualized volatility')
plt.xlabel('date')
plt.axvline(pd.to_datetime('2025-01-01'), color='black', linestyle='--', linewidth=1)
plt.axvline(pd.to_datetime('2025-06-01'), color='black', linestyle='--', linewidth=1)
plt.axvspan(pd.to_datetime('2025-01-01'), pd.to_datetime('2025-06-01'), color='gray', alpha=0.2)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/aggregate-fxvolatility-rolling.png')
