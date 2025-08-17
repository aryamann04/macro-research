import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

from data.fredconnect import fred
from data.loader import get_spots 

spots = get_spots()
spots['USD/EUR'] = 1 / spots['EUR/USD']
spots['USD/GBP'] = 1 / spots['GBP/USD']

daily_yield = fred.get_series('DGS10').to_frame(name='10yr_U.S._nominal_rate')
daily_yield.index = pd.to_datetime(daily_yield.index)
daily_yield.dropna(inplace=True)

date_ranges = [('2008-08-01', '2009-05-01'), ('2020-02-01', '2020-07-01'), ('2025-03-20', '2025-05-10')]
pairs = ['USD/EUR', 'USD/GBP', 'USD/YEN', 'USD/YUAN']
windows = [21, 63, 126, 252] # 1m, 3m, 6m, 1y

def plot_rolling_correlations(start=None, end=None, full=False): 
    fig_lvl, axes_lvl = plt.subplots(2, 2, figsize=(14, 9))
    axes_lvl = axes_lvl.ravel()

    fig_ret, axes_ret = plt.subplots(2, 2, figsize=(14, 9))
    axes_ret = axes_ret.ravel()

    for i, c in enumerate(pairs): 
        aligned = pd.concat([spots[c], daily_yield], axis=1).dropna()
        lr = np.log(aligned).diff().dropna()

        for w in windows:
            rc_lvl = aligned[c].rolling(w).corr(aligned['10yr_U.S._nominal_rate'])
            rc_ret = lr[c].rolling(w).corr(lr['10yr_U.S._nominal_rate'])
            
            if start and end: 
                rc_lvl = rc_lvl.truncate(before=start, after=end)
                rc_ret = rc_ret.truncate(before=start, after=end)

            axes_lvl[i].plot(rc_lvl, label=f'{w} days', color='red', alpha=w/252)
            axes_ret[i].plot(rc_ret, label=f'{w} days', color='red', alpha=w/252)
        
        if full: 
            for start_d, end_d in date_ranges:
                start_ts, end_ts = pd.to_datetime(start_d), pd.to_datetime(end_d)
                axes_lvl[i].axvspan(start_ts, end_ts, color='gray', alpha=0.2, zorder=0)
                axes_ret[i].axvspan(start_ts, end_ts, color='gray', alpha=0.2, zorder=0)
        
        for ax in (axes_lvl[i], axes_ret[i]):
            ax.set_ylim(-1.05, 1.05)
            ax.axhline(0, linestyle='-', linewidth=1, color='black', alpha=0.6, zorder=1.5, label='_nolegend_')
            ax.tick_params(axis='x', labelsize=7)
            ax.grid(True, linestyle='-', alpha=0.3, zorder=1)

        axes_lvl[i].set_title(f'{c}')
        axes_lvl[i].set_xlabel('date')
        axes_lvl[i].set_ylabel('correlation')
        axes_lvl[i].legend(loc='upper left')

        axes_ret[i].set_title(f'{c}')
        axes_ret[i].set_xlabel('date')
        axes_ret[i].set_ylabel('correlation')
        axes_ret[i].legend(loc='upper left')

    if full: 
        fig_lvl.suptitle('rolling correlations: currency pairs vs 10y U.S. treasury yield (levels)', fontsize=14)
        fig_lvl.tight_layout(rect=[0, 0.03, 1, 0.97])

        fig_ret.suptitle('rolling correlations: currency pairs vs 10y U.S. treasury yield (log returns)', fontsize=14)
        fig_ret.tight_layout(rect=[0, 0.03, 1, 0.97])

        fig_lvl.savefig(f'/Users/aryaman/macro-research/plots/figures/correlation/pairs_vs_10yr_rolling_corr_levels')
        fig_ret.savefig(f'/Users/aryaman/macro-research/plots/figures/correlation/pairs_vs_10yr_rolling_corr_logrets')
    else: 
        fig_lvl.suptitle(f'({start} to {end}) rolling correlations: currency pairs vs 10y U.S. treasury yield (levels)', fontsize=14)
        fig_lvl.tight_layout(rect=[0, 0.03, 1, 0.97])

        fig_ret.suptitle(f'({start} to {end}) rolling correlations: currency pairs vs 10y U.S. treasury yield (log returns)', fontsize=14)
        fig_ret.tight_layout(rect=[0, 0.03, 1, 0.97])

        fig_lvl.savefig(f'/Users/aryaman/macro-research/plots/figures/correlation/{start}_pairs_vs_10yr_rolling_corr_levels')
        fig_ret.savefig(f'/Users/aryaman/macro-research/plots/figures/correlation/{start}_pairs_vs_10yr_rolling_corr_logrets')

    plt.show()

plot_rolling_correlations(full=True)

for start, end in date_ranges:
    plot_rolling_correlations(start, end)
