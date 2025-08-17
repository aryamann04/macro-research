import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 

from vol_models.arch_vol import log_rets, get_arch_vols
from data.loader import get_spots

rets = log_rets(get_spots()).truncate(before='2006-01-01')
arch_vols = get_arch_vols(rets)

fig, ax = plt.subplots(figsize=(12, 6))
arch_vols['EUR/USD'].plot(ax=ax, color='blue', alpha=0.7)
arch_vols['GBP/USD'].plot(ax=ax, color='green', alpha=0.7)
arch_vols['USD/YEN'].plot(ax=ax, color='red', alpha=0.7)
arch_vols['USD/YUAN'].plot(ax=ax, color='orange', alpha=0.7)

highlight_ranges = [
    ('2008-08-01', '2009-05-01'),
    ('2020-02-01', '2020-07-01'),
    ('2025-03-20', '2025-05-10')
]

for start, end in highlight_ranges:
    plt.axvspan(pd.to_datetime(start), pd.to_datetime(end), color='gray', alpha=0.2)

ax.set_title('ARCH conditional volatilities')
ax.set_ylabel('volatility (%)')
ax.set_xlabel('date')
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/ARCH/ARCH_vols_daily.png')

# plot monthly annualized vol with monthly annualized ARCH vols

fxvol_by_month = rets.pow(2).resample('M').mean().mul(252).pow(0.5)
arch_vols_annualized = arch_vols.mul(np.sqrt(252))

plt.figure(figsize=(10, 5))

fxvol_by_month['EUR/USD'].plot(label='EUR/USD realized vol', color='blue', linestyle='--', alpha=0.7)
arch_vols_annualized['EUR/USD'].plot(label='EUR/USD ARCH vol', color='blue', linestyle='-', linewidth=1)

fxvol_by_month['GBP/USD'].plot(label='GBP/USD realized vol', color='green', linestyle='--', alpha=0.7)
arch_vols_annualized['GBP/USD'].plot(label='GBP/USD ARCH vol', color='green', linestyle='-', linewidth=1)

fxvol_by_month['USD/YEN'].plot(label='USD/YEN realized vol', color='red', linestyle='--', alpha=0.7)
arch_vols_annualized['USD/YEN'].plot(label='USD/YEN ARCH vol', color='red', linestyle='-', linewidth=1)

fxvol_by_month['USD/YUAN'].plot(label='USD/YUAN realized vol', color='orange', linestyle='--', alpha=0.7)
arch_vols_annualized['USD/YUAN'].plot(label='USD/YUAN ARCH vol', color='orange', linestyle='-', linewidth=1)

for start, end in highlight_ranges:
    plt.axvspan(pd.to_datetime(start), pd.to_datetime(end), color='gray', alpha=0.2)

plt.title('monthly annualized realized volatility (dashed) vs ARCH volatility (solid)')
plt.ylabel('annualized volatility (%)')
plt.xlabel('date')
plt.legend(loc='upper left')
plt.tight_layout()
# plt.savefig('/Users/aryaman/macro-research/plots/figures/ARCH/ARCH_vols_monthly.png')
plt.show()

# split into subplots 

# fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
# axes = axes.ravel()