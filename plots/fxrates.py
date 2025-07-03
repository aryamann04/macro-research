import pandas as pd 
import matplotlib.pyplot as plt 
from realrates import realrates 

# load data

usd_yen = pd.read_csv('/Users/aryaman/macro-research/data/usd-yen.csv', index_col=0, parse_dates=True)
usd_eur = pd.read_csv('/Users/aryaman/macro-research/data/usd-eur.csv', index_col=0, parse_dates=True)
usd_gbp = pd.read_csv('/Users/aryaman/macro-research/data/usd-gbp.csv', index_col=0, parse_dates=True)
usd_yuan = pd.read_csv('/Users/aryaman/macro-research/data/usd-yuan.csv', index_col=0, parse_dates=True)

fxrates = pd.DataFrame()
fxrates['USD/YEN'] = usd_yen['CCUSMA02JPM618N']
fxrates['USD/EUR'] = usd_eur['CCUSMA02EZM618N']
fxrates['USD/GBP'] = usd_gbp['CCUSMA02GBM618N']
fxrates['USD/YUAN'] = usd_yuan['CCUSMA02CNM618N']

# by convention, eur/usd and gbp/usd are quoted per unit usd 
fxrates['EUR/USD'] = 1 / fxrates['USD/EUR']
fxrates['GBP/USD'] = 1 / fxrates['USD/GBP']

# plots 

plt.figure(figsize=(10, 5))
fxrates['USD/GBP'].plot(label='USD/GBP', color='orange')
plt.title('USD/GBP')
plt.xlabel('date')
plt.ylabel('pound sterling per USD')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usd-gbp.png')
# plt.show()

plt.figure(figsize=(10, 5))
fxrates['USD/YUAN'].dropna().plot(label='USD/YUAN', color='orange')
plt.title('USD/YUAN')
plt.xlabel('date')
plt.ylabel('yuan reminbi per USD')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usd-yuan.png')
# plt.show()

plt.figure(figsize=(10, 5))
fxrates['USD/EUR'].dropna().plot(label='USD/EUR', color='orange')
plt.title('USD/EUR')
plt.xlabel('date')
plt.ylabel('euro per USD')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usd-eur.png')
# plt.show()

plt.figure(figsize=(10, 5))
fxrates['USD/YEN'].plot(label='USD/YEN', color='orange')
plt.title('USD/YEN')
plt.xlabel('date')
plt.ylabel('yen per USD')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usd-yen.png')
# plt.show()

plt.figure(figsize=(10, 5))
fxrates['EUR/USD'].dropna().plot(label='EUR/USD', color='orange')
plt.title('EUR/USD')
plt.xlabel('date')
plt.ylabel('USD per euro')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/eur-usd.png')
# plt.show()

plt.figure(figsize=(10, 5))
fxrates['GBP/USD'].dropna().plot(label='GBP/USD', color='orange')
plt.title('GBP/USD')
plt.xlabel('date')
plt.ylabel('USD per pound sterling')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/gbp-usd.png')
# plt.show()

# dual axis plot with real rates

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
fxrates['USD/YEN'].plot(ax=ax1, label='USD/YEN', color='orange')
realrates['10yr_real_cpi'].plot(ax=ax2, linestyle='--', label='10yr real rate with CPI', color='green')
realrates['10yr_real_corecpi'].plot(ax=ax2, linestyle='--', label='10yr real rate (core CPI)', color='blue')
realrates['10yr_real_pce'].plot(ax=ax2, linestyle='--', label='10yr real rate (PCE)', color='red')
ax1.set_title('USD/YEN and 10yr Real Rates')
ax1.set_xlabel('date')
ax1.set_ylabel('yen per USD')
ax2.set_ylabel('real rate (%)')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usd-yen-realrates.png')
# plt.show()

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
fxrates['USD/GBP'].plot(ax=ax1, label='USD/GBP', color='orange')
realrates['10yr_real_cpi'].plot(ax=ax2, linestyle='--', label='10yr real rate with CPI', color='green')
realrates['10yr_real_corecpi'].plot(ax=ax2, linestyle='--', label='10yr real rate (core CPI)', color='blue')
realrates['10yr_real_pce'].plot(ax=ax2, linestyle='--', label='10yr real rate (PCE)', color='red')
ax1.set_title('USD/GBP and 10yr Real Rates')
ax1.set_xlabel('date')
ax1.set_ylabel('pound sterling per USD')
ax2.set_ylabel('real rate (%)')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usd-gbp-realrates.png')
# plt.show()

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
fxrates['USD/YUAN'].plot(ax=ax1, label='USD/YUAN', color='orange')
realrates['10yr_real_cpi'].plot(ax=ax2, linestyle='--', label='10yr real rate with CPI', color='green')
realrates['10yr_real_corecpi'].plot(ax=ax2, linestyle='--', label='10yr real rate (core CPI)', color='blue')
realrates['10yr_real_pce'].plot(ax=ax2, linestyle='--', label='10yr real rate (PCE)', color='red')
ax1.set_title('USD/YUAN and 10yr Real Rates')
ax1.set_xlabel('date')
ax1.set_ylabel('yuan reminbi per USD')
ax2.set_ylabel('real rate (%)')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usd-yuan-realrates.png')
# plt.show()

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
fxrates['USD/EUR'].plot(ax=ax1, label='USD/EUR', color='orange')
realrates['10yr_real_cpi'].plot(ax=ax2, linestyle='--', label='10yr real rate with CPI', color='green')
realrates['10yr_real_corecpi'].plot(ax=ax2, linestyle='--', label='10yr real rate (core CPI)', color='blue')
realrates['10yr_real_pce'].plot(ax=ax2, linestyle='--', label='10yr real rate (PCE)', color='red')
ax1.set_title('USD/EUR and 10yr Real Rates')
ax1.set_xlabel('date')
ax1.set_ylabel('euro per USD')
ax2.set_ylabel('real rate (%)')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usd-eur-realrates.png')
# plt.show()