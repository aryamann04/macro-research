import pandas as pd 
import matplotlib.pyplot as plt

from data.fredconnect import fred
from data.loader import get_spots 

spots = get_spots()
spots['USD/EUR'] = 1 / spots['EUR/USD']
spots['USD/GBP'] = 1 / spots['GBP/USD']

daily_yield = fred.get_series('DGS10').to_frame(name='10yr_U.S._nominal_rate')
daily_yield.index = pd.to_datetime(daily_yield.index)
daily_yield.dropna(inplace=True)

date_ranges = [['2008-07-01', '2009-02-28'], ['2020-04-01', '2021-01-31'], ['2025-04-01', '2025-04-30']]
pairs = ['USD/EUR', 'USD/GBP', 'USD/YEN', 'USD/YUAN']

for start, end in date_ranges: 
    spots_trunc = spots.truncate(start, end)
    yield_trunc = daily_yield.truncate(start, end)
    ry = (yield_trunc['10yr_U.S._nominal_rate'].iloc[-1] - yield_trunc['10yr_U.S._nominal_rate'].iloc[0]) / yield_trunc['10yr_U.S._nominal_rate'].iloc[0] * 100
    print(f"\n{start}-{end} yield appreciation: {ry:.2f}%")

    for c in pairs:
        print(f"{c} {start}-{end} appreciation: {(spots_trunc[c].iloc[-1] - spots_trunc[c].iloc[0]) / spots_trunc[c].iloc[0] * 100:.2f}%")
        continue 

        fig, ax1 = plt.subplots(figsize=(10, 5))
        ax2 = ax1.twinx()   
        spots_trunc[c].plot(ax=ax1, color='orange', label=c)
        yield_trunc['10yr_U.S._nominal_rate'].plot(ax=ax2, color='black', linestyle='-', label='10yr U.S. nominal rate')
        ax1.set_xlabel('date')
        ax1.set_ylabel(f'{c}')
        ax2.set_ylabel('10‑yr U.S. nominal rate (%)')
        ax1.set_title(f'{c} vs. 10yr U.S. treasury yield ({start} to {end})')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        
        plt.tight_layout()
        plt.savefig(f'/Users/aryaman/macro-research/plots/figures/focused_plots/{c.replace("/", "-")}-{start}-{end}')
        plt.show()