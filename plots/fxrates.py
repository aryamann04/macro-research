import pandas as pd 
import matplotlib.pyplot as plt

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

print(fxrates.head(10))

# plots 

plt.figure(figsize=(10, 5))
fxrates['USD/GBP'].plot(label='USD/GBP', color='orange')
plt.title('USD/GBP')
plt.xlabel('date')
plt.ylabel('pound sterling per USD')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usd-gbp.png')
plt.show()

plt.figure(figsize=(10, 5))
fxrates['USD/YUAN'].dropna().plot(label='USD/YUAN', color='orange')
plt.title('USD/YUAN')
plt.xlabel('date')
plt.ylabel('yuan reminbi per USD')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usd-yuan.png')
plt.show()

plt.figure(figsize=(10, 5))
fxrates['USD/EUR'].dropna().plot(label='USD/EUR', color='orange')
plt.title('USD/EUR')
plt.xlabel('date')
plt.ylabel('euro per USD')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usd-eur.png')
plt.show()

plt.figure(figsize=(10, 5))
fxrates['USD/YEN'].plot(label='USD/YEN', color='orange')
plt.title('USD/YEN')
plt.xlabel('date')
plt.ylabel('yen per USD')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usd-yen.png')
plt.show()


