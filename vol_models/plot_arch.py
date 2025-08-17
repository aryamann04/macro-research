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
    ('2020-01-01', '2020-07-01'),
    ('2025-03-01', '2025-06-01')
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

fxvol_by_month = rets.resample('M').std(ddof=0).mul(np.sqrt(252))
arch_vols_by_month = arch_vols.resample('M').mean().mul(np.sqrt(252))

plt.figure(figsize=(10, 5))

fxvol_by_month['EUR/USD'].plot(label='EUR/USD realized vol', color='blue', linestyle='--', alpha=0.7)
arch_vols_by_month['EUR/USD'].plot(label='EUR/USD ARCH vol', color='blue', linestyle='-', linewidth=1.5)

fxvol_by_month['GBP/USD'].plot(label='GBP/USD realized vol', color='green', linestyle='--', alpha=0.7)
arch_vols_by_month['GBP/USD'].plot(label='GBP/USD ARCH vol', color='green', linestyle='-', linewidth=1.5)

fxvol_by_month['USD/YEN'].plot(label='USD/YEN realized vol', color='red', linestyle='--', alpha=0.7)
arch_vols_by_month['USD/YEN'].plot(label='USD/YEN ARCH vol', color='red', linestyle='-', linewidth=1.5)

fxvol_by_month['USD/YUAN'].plot(label='USD/YUAN realized vol', color='orange', linestyle='--', alpha=0.7)
arch_vols_by_month['USD/YUAN'].plot(label='USD/YUAN ARCH vol', color='orange', linestyle='-', linewidth=1.5)

highlight_ranges = [
    ('2008-08', '2009-04'),
    ('2020-01', '2020-07'),
    ('2025-03', '2025-05')
]

for start, end in highlight_ranges:
    plt.axvspan(pd.to_datetime(start), pd.to_datetime(end), color='gray', alpha=0.2)

plt.title('monthly annualized realized volatility vs ARCH volatility')
plt.ylabel('annualized volatility (%)')
plt.xlabel('date')
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/ARCH/ARCH_vols_monthly.png')
plt.show()