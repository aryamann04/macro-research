import matplotlib.pyplot as plt

from loader import euro_data, uk_data, japan_data, china_data
from realrates import realrates 
from fxrates import fxrates

# normalize index
realrates = realrates.copy()
realrates.index = realrates.index.to_period('M')

# euro real rates & spreads 
euro_data['10yr_real_hicp'] = euro_data['10yr_yield'] - euro_data['hicp']   
euro_data['10yr_real_core_hicp'] = euro_data['10yr_yield'] - euro_data['core_hicp']

euro_data['10yr_nominal_spread'] = euro_data['10yr_yield'] - realrates['10yr_nominal']
euro_data['10yr_real_cpi_spread'] = euro_data['10yr_real_hicp'] - realrates['10yr_real_cpi']
euro_data['10yr_real_core_cpi_spread'] = euro_data['10yr_real_core_hicp'] - realrates['10yr_real_corecpi']

# uk real rates & spreads
uk_data['10yr_real_cpi'] = uk_data['10yr_yield'] - uk_data['cpi']
uk_data['10yr_real_core_cpi'] = uk_data['10yr_yield'] - uk_data['core_cpi']

uk_data['10yr_nominal_spread'] = uk_data['10yr_yield'] - realrates['10yr_nominal']
uk_data['10yr_real_cpi_spread'] = uk_data['10yr_real_cpi'] - realrates['10yr_real_cpi']
uk_data['10yr_real_core_cpi_spread'] = uk_data['10yr_real_core_cpi'] - realrates['10yr_real_corecpi']

# japan real rates & spreads
japan_data['10yr_real_cpi'] = japan_data['10yr_yield'] - japan_data['cpi']
japan_data['10yr_real_core_cpi'] = japan_data['10yr_yield'] - japan_data['core_cpi']

japan_data['10yr_nominal_spread'] = japan_data['10yr_yield'] - realrates['10yr_nominal']
japan_data['10yr_real_cpi_spread'] = japan_data['10yr_real_cpi'] - realrates['10yr_real_cpi']
japan_data['10yr_real_core_cpi_spread'] = japan_data['10yr_real_core_cpi'] - realrates['10yr_real_corecpi']

# china real rates & spreads
# no core cpi data available for china 
china_data['10yr_real_cpi'] = china_data['10yr_yield'] - china_data['cpi']

china_data['10yr_nominal_spread'] = china_data['10yr_yield'] - realrates['10yr_nominal']
china_data['10yr_real_cpi_spread'] = china_data['10yr_real_cpi'] - realrates['10yr_real_cpi']

# dual axis plots with spreads

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
fxrates['USD/YEN'].plot(ax=ax1, label='USD/YEN', color='orange')
japan_data['10yr_nominal_spread'].plot(ax=ax2, linestyle='--', label='10yr nominal spread', color='black')
japan_data['10yr_real_cpi_spread'].plot(ax=ax2, linestyle='--', label='10yr real rate (CPI) spread', color='green')
japan_data['10yr_real_core_cpi_spread'].plot(ax=ax2, linestyle='--', label='10yr real rate (core CPI) spread', color='blue')
ax1.set_title('USD/YEN and 10yr Japan-US spreads')
ax1.set_xlabel('date')
ax1.set_ylabel('yen')
ax2.set_ylabel('spread (%)')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usd-yen-spreads.png')
# plt.show()

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
fxrates['USD/GBP'].plot(ax=ax1, label='USD/GBP', color='orange')
uk_data['10yr_nominal_spread'].plot(ax=ax2, linestyle='--', label='10yr nominal spread', color='black')
uk_data['10yr_real_cpi_spread'].plot(ax=ax2, linestyle='--', label='10yr real rate (CPI) spread', color='green')
uk_data['10yr_real_core_cpi_spread'].plot(ax=ax2, linestyle='--', label='10yr real rate (core CPI) spread', color='blue')
ax1.set_title('USD/GBP and 10yr Britain-US spreads')
ax1.set_xlabel('date')
ax1.set_ylabel('pound sterling')
ax2.set_ylabel('spread (%)')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usd-gbp-spreads.png')
# plt.show()

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
fxrates['USD/YUAN'].plot(ax=ax1, label='USD/YUAN', color='orange')
china_data['10yr_nominal_spread'].plot(ax=ax2, linestyle='--', label='10yr nominal spread', color='black')
china_data['10yr_real_cpi_spread'].plot(ax=ax2, linestyle='--', label='10yr real rate (CPI) spread', color='green')
ax1.set_title('USD/YUAN and 10yr China-US spreads')
ax1.set_xlabel('date')
ax1.set_ylabel('yuan reminbi')
ax2.set_ylabel('spread (%)')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usd-yuan-spreads.png')
# plt.show()

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
fxrates['USD/EUR'].plot(ax=ax1, label='USD/EUR', color='orange')
euro_data['10yr_nominal_spread'].plot(ax=ax2, linestyle='--', label='10yr nominal spread', color='black')
euro_data['10yr_real_cpi_spread'].plot(ax=ax2, linestyle='--', label='10yr real rate (CPI) spread', color='green')
euro_data['10yr_real_core_cpi_spread'].plot(ax=ax2, linestyle='--', label='10yr real rate (core CPI) spread', color='blue')
ax1.set_title('USD/EUR and 10yr Europe-US spreads')
ax1.set_xlabel('date')
ax1.set_ylabel('euro')
ax2.set_ylabel('spread (%)')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/usd-eur-spreads.png')
# plt.show()