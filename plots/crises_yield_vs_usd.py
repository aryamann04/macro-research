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

date_ranges = [['GFC', '2008-08-01', '2009-05-01'], ['COVID', '2020-02-01', '2020-07-01'], ['April 2025', '2025-03-20', '2025-05-10']]
pairs = ['USD/EUR', 'USD/GBP', 'USD/YEN', 'USD/YUAN']

for label, start, end in date_ranges:
    spots_trunc = spots.truncate(start, end)
    yield_trunc = daily_yield.truncate(start, end)

    # percent change in yield 
    ry = (yield_trunc['10yr_U.S._nominal_rate'].iloc[-1] - yield_trunc['10yr_U.S._nominal_rate'].iloc[0]) / yield_trunc['10yr_U.S._nominal_rate'].iloc[0] * 100

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    axes = axes.ravel()

    summary_rows = []

    for i, c in enumerate(pairs):
        # percent change in currency pair 
        rc = (spots_trunc[c].iloc[-1] - spots_trunc[c].iloc[0]) / spots_trunc[c].iloc[0] * 100

        # correlations - level and log returns (with and without lags)
        aligned = pd.concat([spots_trunc[c].rename('spot'), yield_trunc], axis=1).dropna()
        corr_level = aligned['spot'].corr(aligned['10yr_U.S._nominal_rate'])
        corr_level_lag1 = aligned['spot'].corr(aligned['10yr_U.S._nominal_rate'].shift(1)) 

        lr = np.log(aligned).diff().dropna()
        corr_logret = lr['spot'].corr(lr['10yr_U.S._nominal_rate'])
        corr_logret_lag1 = lr['spot'].corr(lr['10yr_U.S._nominal_rate'].shift(1))

        summary_rows.append(  
            (c, rc, ry, len(aligned), corr_level, corr_level_lag1, corr_logret, corr_logret_lag1)
        )

        ax1 = axes[i]
        ax2 = ax1.twinx()   
        spots_trunc[c].plot(ax=ax1, color='orange', label=c)
        yield_trunc['10yr_U.S._nominal_rate'].plot(ax=ax2, color='black', linestyle='-', label='10yr U.S. nominal rate')
        ax1.set_xlabel('date')
        ax1.set_ylabel(f'{c}')
        ax2.set_ylabel('10-yr U.S. nominal rate (%)')
        ax1.set_title(f'{c}')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
    
    summary = pd.DataFrame( 
        summary_rows,
        columns=[
            'pair', 'USD vs pair %', '10y yield %', 'n',
            'corr(level)', 'corr(level, yield -1d)',
            'corr(logret)', 'corr(logret, yield -1d)'
        ]
    ).set_index('pair').round(2)

    print(f"\n{label}\n")
    print(summary)

    fig.tight_layout(rect=[0, 0.03, 1, 0.97])
    fig.suptitle(f'{label}: currency pairs vs 10y U.S. treasury yield ({start} to {end})', fontsize=14)
    plt.savefig(f'/Users/aryaman/macro-research/plots/figures/focused_plots/pairs_vs_10yr_{label}')
    plt.show()