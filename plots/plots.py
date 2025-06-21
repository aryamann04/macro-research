import pandas as pd 
import matplotlib.pyplot as plt

# 10yr yield, 10 yr real interest rate

wrds_fed_yield_data = pd.read_csv('/Users/aryaman/macro-research/data/treasuryyields.csv', index_col=0, parse_dates=True)

plt.figure(figsize=(10,5))
wrds_fed_yield_data['fii10'].plot(label='fii10', color='blue')
wrds_fed_yield_data['gs10'].plot(label='gs10', color='green')
wrds_fed_yield_data['reaintratrearat10y'].plot(label='real 10yr rate', color='red')
plt.title('wrds yield and real rate data')
plt.xlabel('date')
plt.ylabel('rate (%)')
plt.legend() 
plt.tight_layout()
plt.show()

# Exchange Rates 

fxrates = pd.read_csv('/Users/aryaman/macro-research/data/fxrates.csv', index_col=0, parse_dates=True)

plt.figure(figsize=(10, 5))
fxrates['exukus'].plot(label='GBP/USD', color='orange')
plt.title('GBP/USD')
plt.xlabel('Date')
plt.ylabel('Exchange Rate')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/gbp-usd.png')
plt.show()

plt.figure(figsize=(10, 5))
fxrates['exchus'].dropna().plot(label='YUAN/USD', color='orange')
plt.title('YUAN/USD')
plt.xlabel('Date')
plt.ylabel('Exchange Rate')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/yuan-usd.png')
plt.show()

plt.figure(figsize=(10, 5))
fxrates['exeuus'].dropna().plot(label='EUR/USD', color='orange')
plt.title('EUR/USD')
plt.xlabel('Date')
plt.ylabel('Exchange Rate')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/eur-usd.png')
plt.show()

plt.figure(figsize=(10, 5))
fxrates['exjpus'].plot(label='YEN/USD', color='orange')
plt.title('YEN/USD')
plt.xlabel('Date')
plt.ylabel('Exchange Rate')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/yen-usd.png')
plt.show()


