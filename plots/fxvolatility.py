import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import levene, fligner 
from fredconnect import fred

# connect via FRED API
series = ['DEXUSEU', 'DEXUSUK', 'DEXJPUS', 'DEXCHUS']
spot_data = {sid: fred.get_series(sid) for sid in series}
spots = pd.DataFrame(spot_data)

spots = spots.rename(columns={
    'DEXUSEU': 'EUR/USD',
    'DEXUSUK': 'GBP/USD',
    'DEXJPUS': 'USD/YEN',
    'DEXCHUS': 'USD/YUAN'
})

spots.index = pd.to_datetime(spots.index)
spots.dropna(inplace=True)
spots = spots.truncate(before='2007-01-01')

# log returns 
spots = np.log(spots).diff().dropna()

spots_2024 = spots[spots.index.year == 2024]
spots_2025 = spots[spots.index.year == 2025]

# calculate observed vol for 2025 using all data pts 
vol_2025 = spots_2025.std() * np.sqrt(252)

n = len(spots_2025)
B = 10000
boot_vols = [] 

for i in range(B): 
    sample = spots_2024.sample(n=n, replace=True)
    boot_vol = sample.std() * np.sqrt(252)
    boot_vols.append(boot_vol)

boot_vols = pd.DataFrame(boot_vols)
boot_mean = boot_vols.mean()

# hypothesis testing via bootstrapping
p_vals = {}
for c in spots.columns: 
    obs = vol_2025[c]
    mu = boot_mean[c]
    p_vals[c] = np.mean(np.abs(boot_vols[c] - mu) >= np.abs(obs - mu))

test1 = pd.DataFrame({
    '2025_vol': vol_2025,
    '2024_boot_vol_mean': boot_mean,
    'diff': vol_2025 - boot_mean,
    'p_value': p_vals
})

pd.set_option('display.float_format', '{:.6}'.format)
print(test1)

# levene & fligner tests -- robust to departure from normality 

results = []
for c in spots.columns:
    r24 = spots_2024[c].values
    r25 = spots_2025[c].values

    W, p_l = levene(r24, r25, center='median')
    F, p_f = fligner(r24, r25)

    results.append({
        'pair': c,
        'levene_p_val': p_l,
        'fligner_p_val': p_f
    })

test2 = pd.DataFrame(results).set_index('pair')
print(test2)

'''
# vol by year - whole sample

fxvol_by_year = spots.groupby(spots.index.year).std().mul(np.sqrt(252))
fxvol_by_year.index = pd.to_datetime(fxvol_by_year.index.astype(str) + '-12-31')
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
'''