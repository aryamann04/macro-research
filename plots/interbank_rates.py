import pandas as pd 
import matplotlib.pyplot as plt 

from data.loader import get_interbank_rates

interbank_rates = get_interbank_rates()

fig, ax = plt.subplots(figsize=(12, 6))
interbank_rates['US - Euro area'] = interbank_rates['US interbank rate'] - interbank_rates['Euro area interbank rate']
interbank_rates['US - UK'] = interbank_rates['US interbank rate'] - interbank_rates['UK interbank rate']
interbank_rates['US - Japan'] = interbank_rates['US interbank rate'] - interbank_rates['Japan interbank rate']
interbank_rates['US - China'] = interbank_rates['US interbank rate'] - interbank_rates['China interbank rate']

interbank_rates = interbank_rates.truncate(before='2002-01-01', after='2009-06-01')

interbank_rates['US - Euro area'].plot(ax=ax, alpha=0.7, color='blue')
interbank_rates['US - UK'].plot(ax=ax, alpha=0.7, color='green')
interbank_rates['US - Japan'].plot(ax=ax, alpha=0.7, color='red')
interbank_rates['US - China'].plot(ax=ax, alpha=0.7, color='orange')

plt.axvspan(pd.to_datetime('2008-08-01'), pd.to_datetime('2009-05-01'), color='gray', alpha=0.2)
ax.axhline(0, linestyle='-', linewidth=1, color='black', alpha=0.6, zorder=1.5, label='_nolegend_')

ax.set_title('interbank rate differentials leading to GFC')
ax.set_ylabel('differential (%)')
ax.set_xlabel('date')
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/interbank_rates_differentials_GFC.png')
plt.show()