import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 

from vol_models.ARCH.arch_vol import log_rets, get_arch_vols
from vol_models.GARCH.garch_vol import get_garch_egarch_vols
from data.loader import get_spots

rets = log_rets(get_spots()).truncate(before='2006-01-01')

arch_vols, _ = get_arch_vols(rets)
garch_egarch, _ = get_garch_egarch_vols(rets)
garch_vols = garch_egarch['GARCH']
egarch_vols = garch_egarch['EGARCH']

highlight_ranges = [
        ('2008-08-01', '2009-05-01'),
        ('2020-02-01', '2020-07-01'),
        ('2025-03-31', '2025-05-10')
    ]

def plot_all_vols(model): 
    fig, ax = plt.subplots(figsize=(12, 6))

    if model == 'ARCH':
        vols = arch_vols
    elif model == 'GARCH':
        vols = garch_vols
    elif model == 'EGARCH':
        vols = egarch_vols
    
    vols['EUR/USD'].plot(ax=ax, color='blue', alpha=0.7)
    vols['GBP/USD'].plot(ax=ax, color='green', alpha=0.7)
    vols['USD/YEN'].plot(ax=ax, color='red', alpha=0.7)
    vols['USD/YUAN'].plot(ax=ax, color='orange', alpha=0.7)

    for start, end in highlight_ranges:
        plt.axvspan(pd.to_datetime(start), pd.to_datetime(end), color='gray', alpha=0.2)

    ax.set_title(f'{model} conditional volatilities')
    ax.set_ylabel('volatility (%)')
    ax.set_xlabel('date')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(f'/Users/aryaman/macro-research/plots/figures/{model}/{model}_vols_daily.png')
    plt.show()

# plot_all_vols('ARCH')
# plot_all_vols('GARCH')
plot_all_vols('EGARCH')

# plot monthly annualized vol with annualized ARCH vols

def plot_realized_and_arch(start=None, end=None, full=True):

    fxvol_by_month = rets.pow(2).resample('M').mean().mul(252).pow(0.5)
    arch_vols_annualized = arch_vols.pow(2).resample('M').mean().mul(252).pow(0.5)

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
    # plot_realized_and_arch(start=s, end=e, full=False)

def plot_vols_by_pair_rolling(rets, arch_vols, garch_vols, egarch_vols, start=None, end=None, pairs=None):
    rv21 = rets.pow(2).rolling(21).mean().mul(252).pow(0.5)
    arch21 = arch_vols.pow(2).rolling(21).mean().mul(252).pow(0.5)
    garch21 = garch_vols.pow(2).rolling(21).mean().mul(252).pow(0.5)
    egarch21 = egarch_vols.pow(2).rolling(21).mean().mul(252).pow(0.5)

    if start or end:
        s = pd.to_datetime(start) if start is not None else None
        e = pd.to_datetime(end) if end is not None else None
        rv21 = rv21.loc[s:e]
        arch21 = arch21.loc[s:e]
        garch21 = garch21.loc[s:e]
        egarch21 = egarch21.loc[s:e]

    if pairs is None:
        pairs = [p for p in ['EUR/USD','GBP/USD','USD/YEN','USD/YUAN'] if p in rets.columns]

    for pair in pairs:
        fig, ax = plt.subplots(figsize=(10,5))

        rv21[pair].dropna().plot(ax=ax, linestyle='--', label='Realized (21D)')
        arch21[pair].dropna().plot(ax=ax, label='ARCH (21D)')
        garch21[pair].dropna().plot(ax=ax, label='GARCH (21D)')
        egarch21[pair].dropna().plot(ax=ax, label='EGARCH (21D)')

        ax.axvspan(pd.to_datetime(start) + pd.DateOffset(months=2), pd.to_datetime(end) - pd.DateOffset(months=2), color='gray', alpha=0.2)
        ax.set_title(f'{pair}: 21D rolling realized vs model vols (annualized)')
        ax.set_ylabel('annualized volatility (%)')
        ax.set_xlabel('date')
        ax.legend(loc='upper left')

        plt.tight_layout()
        fig.savefig(f'/Users/aryaman/macro-research/plots/figures/GARCH/{start}_{pair.replace("/", "-")}_rolling21_vols.png')
        plt.show()
        plt.close(fig)

for start, end in highlight_ranges:
    s = pd.Timestamp(start) - pd.DateOffset(months=2)
    e = pd.Timestamp(end) + pd.DateOffset(months=2)
    plot_vols_by_pair_rolling(rets, arch_vols, garch_vols, egarch_vols, start=s, end=e)
