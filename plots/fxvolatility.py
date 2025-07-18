import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from scipy.stats import norm, skew, kurtosis, probplot, levene, fligner
from loader import spots 

spots = spots.truncate(before='2007-01-01')

# log returns 
spots = np.log(spots).diff().dropna()

spots_2024 = spots[spots.index.year == 2024]
spots_2025 = spots[spots.index.year == 2025]

# calculate observed vol for 2025 using all data pts 
vol_2025 = spots_2025.std() * np.sqrt(252)

n = len(spots_2025)
print(n)
B = 10000
boot_vols = {c: [] for c in spots.columns}

for i in range(B): 
    sample = spots_2024.sample(n=n, replace=True)
    for c in spots.columns:
        boot_vols[c].append(sample[c].std() * np.sqrt(252))

boot_vols = pd.DataFrame(boot_vols)
boot_mean = boot_vols.mean()

# plot histograms 
for c in spots.columns: 
    plt.figure()
    plt.hist(boot_vols[c], bins=50, alpha=0.7, color='blue', label='bootstrapped volatilities (2024)')
    plt.axvline(vol_2025[c], color='black', linestyle='--', label='observed volatility (2025)')
    plt.title(f'{c} bootstrapped volatilities (2024)')
    plt.xlabel('annualized volatility')
    plt.ylabel('frequency')
    # plt.savefig(f'/Users/aryaman/macro-research/plots/figures/fxvoltests/{c.replace("/", "_")}-bootstrapped-vols.png')
    # plt.show()

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
    'pct change' : (vol_2025 - boot_mean) / boot_mean * 100,
    'p_value': p_vals
})

pd.set_option('display.float_format', '{:0.6}'.format)
print(test1)
print()

# normality checks

for c in spots.columns:
    data = spots[c]
    mu, sigma = data.mean(), data.std()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # histogram vs normal pdf
    axes[0].hist(data, bins=30, density=True, alpha=0.6)
    x = np.linspace(data.min(), data.max(), 200)
    axes[0].plot(x, norm.pdf(x, mu, sigma), linestyle='dashed')
    axes[0].set_title(f'{c} histogram')
    axes[0].set_xlabel('returns')
    axes[0].set_ylabel('density')

    # Q-Q
    probplot(data, dist='norm', plot=axes[1])
    axes[1].set_title(f'{c} Q–Q Plot')

    plt.tight_layout()
    # plt.savefig(f'/Users/aryaman/macro-research/plots/figures/fxvoltests/normality-checks/{c.replace("/", "_")}.png')
    # plt.show()

    sk = skew(data)
    kt = kurtosis(data, fisher=False) 
    # print(f'{c} - skewness: {sk:.4f}, kurtosis: {kt:.4f}')

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
print()
print(test2)

fxvol_by_year = spots.groupby(spots.index.year).std().mul(np.sqrt(252))
fxvol_by_year.index = pd.to_datetime(fxvol_by_year.index.astype(str) + '-12-31')

# vol by year - whole sample


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

# aggregate volatility monthly with average

plt.figure(figsize=(10, 5))

x = agg_monthly_vol.index
plt.plot(x, agg_monthly_vol.values, label='average annualized volatility', color='black', linewidth=2)
plt.plot(x, fxvol_by_month.loc[x, 'EUR/USD'].values, label='EUR/USD', color='blue', linestyle='--', linewidth=1)
plt.plot(x, fxvol_by_month.loc[x, 'GBP/USD'].values, label='GBP/USD', color='green', linestyle='--', linewidth=1)
plt.plot(x, fxvol_by_month.loc[x, 'USD/YEN'].values, label='USD/YEN', color='red', linestyle='--', linewidth=1)
plt.plot(x, fxvol_by_month.loc[x, 'USD/YUAN'].values, label='USD/YUAN', color='orange', linestyle='--', linewidth=1)


plt.title('monthly volatility')
plt.ylabel('annualized volatility')
plt.xlabel('date')

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.tick_params(axis='x', labelsize=8)
plt.xticks(rotation=45, ha='right')

highlight_ranges = [
    ('2008-10', '2009-04'),
    ('2016-04', '2016-10'),
    ('2020-01', '2020-07'),
    ('2022-10', '2023-04'),
    ('2025-01', '2025-07')
]

for start, end in highlight_ranges:
    plt.axvspan(pd.to_datetime(start), pd.to_datetime(end), color='gray', alpha=0.2)

plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/aggregate-monthly-with-avg.png')

