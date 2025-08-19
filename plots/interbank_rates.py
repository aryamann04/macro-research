import pandas as pd 
import matplotlib.pyplot as plt 

from data.loader import get_overnight_interbank_rates, get_3m_interbank_rates

def plot_interbank(start, end, three_month: bool = True):
    if three_month: 
        interbank_rates = get_3m_interbank_rates()
        title = '3-month interbank rate differentials'
        fig_name = '3m_interbank_rates_COVID.png'
    else: 
        interbank_rates = get_overnight_interbank_rates()
        title = 'overnight interbank rate differentials'
        fig_name = 'overnight_interbank_rates_COVID.png'

    fig, ax = plt.subplots(figsize=(12, 6))
    interbank_rates['US - Euro area'] = interbank_rates['US interbank rate'] - interbank_rates['Euro area interbank rate']
    interbank_rates['US - UK'] = interbank_rates['US interbank rate'] - interbank_rates['UK interbank rate']
    interbank_rates['US - Japan'] = interbank_rates['US interbank rate'] - interbank_rates['Japan interbank rate']
    interbank_rates['US - China'] = interbank_rates['US interbank rate'] - interbank_rates['China interbank rate']

    interbank_rates = interbank_rates.truncate(before=start, after=end)

    interbank_rates['US - Euro area'].plot(ax=ax, alpha=0.7, color='blue')
    interbank_rates['US - UK'].plot(ax=ax, alpha=0.7, color='green')
    interbank_rates['US - Japan'].plot(ax=ax, alpha=0.7, color='red')
    interbank_rates['US - China'].plot(ax=ax, alpha=0.7, color='orange')

    # plt.axvspan(pd.to_datetime('2008-08-01'), pd.to_datetime('2009-05-01'), color='gray', alpha=0.2)
    plt.axvspan(pd.to_datetime('2020-02-01'), pd.to_datetime('2020-07-01'), color='gray', alpha=0.2)

    ax.axhline(0, linestyle='-', linewidth=1, color='black', alpha=0.6, zorder=1.5, label='_nolegend_')

    ax.set_title(title)
    ax.set_ylabel('differential (%)')
    ax.set_xlabel('date')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(f'/Users/aryaman/macro-research/plots/figures/{fig_name}')
    plt.show()

# plot_interbank('2002-01-01', '2009-06-01', three_month=False)
# plot_interbank('2002-01-01', '2009-06-01', three_month=True)

plot_interbank('2018-01-01', '2021-01-01', three_month=False)
plot_interbank('2018-01-01', '2021-01-01', three_month=True)

