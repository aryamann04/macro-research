import pandas as pd 
import matplotlib.pyplot as plt

# load data, truncate data to start from 1995-01-01

cutoff_date = '1995-01-01'

fxrates = pd.read_csv('/Users/aryaman/macro-research/data/fxrates.csv', index_col=0, parse_dates=True)
fxrates = fxrates.truncate(before=cutoff_date)

# plots 

plt.figure(figsize=(10, 5))
fxrates['exukus'].plot(label='GBP/USD', color='orange')
plt.title('GBP/USD')
plt.xlabel('date')
plt.ylabel('exchange rate')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/gbp-usd.png')
plt.show()

plt.figure(figsize=(10, 5))
fxrates['exchus'].dropna().plot(label='YUAN/USD', color='orange')
plt.title('YUAN/USD')
plt.xlabel('date')
plt.ylabel('exchange rate')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/yuan-usd.png')
plt.show()

plt.figure(figsize=(10, 5))
fxrates['exeuus'].dropna().plot(label='EUR/USD', color='orange')
plt.title('EUR/USD')
plt.xlabel('date')
plt.ylabel('exchange rate')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/eur-usd.png')
plt.show()

plt.figure(figsize=(10, 5))
fxrates['exjpus'].plot(label='YEN/USD', color='orange')
plt.title('YEN/USD')
plt.xlabel('date')
plt.ylabel('exchange rate')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/yen-usd.png')
plt.show()


