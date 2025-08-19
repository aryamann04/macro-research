import numpy as np
import pandas as pd 
import matplotlib as mpl
import matplotlib.pyplot as plt 

from vol_models.ARCH.arch_vol import log_rets, get_arch_vols
from data.loader import get_spots

rets = log_rets(get_spots()).truncate(before='2006-01-01')
arch_vols, _ = get_arch_vols(rets)

fig, ax = plt.subplots(figsize=(12, 6))
arch_vols['EUR/USD'].plot(ax=ax, color='blue', alpha=0.7)
arch_vols['GBP/USD'].plot(ax=ax, color='green', alpha=0.7)
arch_vols['USD/YEN'].plot(ax=ax, color='red', alpha=0.7)
arch_vols['USD/YUAN'].plot(ax=ax, color='orange', alpha=0.7)

highlight_ranges = [
    ('2008-08-01', '2009-05-01'),
    ('2020-02-01', '2020-07-01'),
    ('2025-03-31', '2025-05-10')
]

for start, end in highlight_ranges:
    plt.axvspan(pd.to_datetime(start), pd.to_datetime(end), color='gray', alpha=0.2)

ax.set_title('ARCH conditional volatilities')
ax.set_ylabel('volatility (%)')
ax.set_xlabel('date')
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/ARCH/ARCH_vols_daily.png')

# plot monthly annualized vol with annualized ARCH vols

def plot_realized_and_arch(start=None, end=None, full=True):

    fxvol_by_month = rets.pow(2).resample('M').mean().mul(252).pow(0.5)
    arch_vols_annualized = arch_vols.mul(np.sqrt(252))

    if start and end:
        fxvol_by_month = fxvol_by_month.loc[start:end]
        arch_vols_annualized = arch_vols_annualized.loc[start:end]

    fig, ax = plt.subplots(figsize=(10, 5))

    pairs = [
        ('EUR/USD', 'blue'),
        ('GBP/USD', 'green'),
        ('USD/YEN', 'red'),
        ('USD/YUAN', 'orange'),
    ]

    for pair, color in pairs:
        m = fxvol_by_month[pair].dropna()
        ax.plot(m.index, m.values, linestyle='--', marker='o', markersize=2, alpha=0.8, color=color, label=f'{pair} realized (monthly)')

        d = arch_vols_annualized[pair].dropna()
        ax.plot(d.index, d.values, linewidth=1.0, color=color, label=f'{pair} ARCH (daily)')

    if full:
        for s, e in highlight_ranges:
            ax.axvspan(pd.to_datetime(s), pd.to_datetime(e), color='gray', alpha=0.2)
    else: 
        ax.axvspan(pd.to_datetime(start) + pd.DateOffset(months=2), pd.to_datetime(end) - pd.DateOffset(months=2), color='gray', alpha=0.2)

    ax.set_ylabel('annualized volatility (%)')
    ax.set_xlabel('date')
    ax.legend(loc='upper right')

    if full:
        plt.title('Monthly realized (dashed) vs daily ARCH (solid)')
        fig.savefig('/Users/aryaman/macro-research/plots/figures/ARCH/ARCH_vols_mnth_vs_daily.png')
    else:
        plt.title(f'({start.date()} to {end.date()}) Monthly realized (dashed) vs daily ARCH (solid)')
        fig.savefig(f'/Users/aryaman/macro-research/plots/figures/ARCH/{start.date()}_ARCH_vols_mnth_vs_daily.png')

    plt.show()

for start, end in highlight_ranges:
    s = pd.Timestamp(start) - pd.DateOffset(months=2)  
    e = pd.Timestamp(end)   + pd.DateOffset(months=2)  
    plot_realized_and_arch(start=s, end=e, full=False)