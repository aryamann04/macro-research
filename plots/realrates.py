import pandas as pd
import matplotlib.pyplot as plt 

from loader import inflation, yields 

# truncate to start from cutoff date '1991-01-01'
cutoff_date = '1991-01-01'
inflation = inflation.truncate(before=cutoff_date)
yields = yields.truncate(before=cutoff_date)

# join inflation and yields, calculate real rates

inflation_and_yields = inflation.join(yields, how='left').dropna()

realrates = pd.DataFrame()
realrates['10yr_nominal'] = inflation_and_yields['10yr_yield']

realrates['10yr_real_pce'] = inflation_and_yields['10yr_yield'] - inflation_and_yields['pce']
realrates['10yr_real_corecpi'] = inflation_and_yields['10yr_yield'] - inflation_and_yields['corecpi']
realrates['10yr_real_cpi'] = inflation_and_yields['10yr_yield'] - inflation_and_yields['cpi']
realrates['10yr_real_corepce'] = inflation_and_yields['10yr_yield'] - inflation_and_yields['corepce']
realrates['10yr_real_cpi_urban'] = inflation_and_yields['10yr_yield'] - inflation_and_yields['cpi_urban']

# real rate plot (all 5 series)

plt.figure(figsize=(10,5))

realrates['10yr_nominal'].plot(label='10yr nominal rate', color='black')

realrates['10yr_real_pce'].plot(label='10yr real rate with PCE', color='red')
realrates['10yr_real_corecpi'].plot(label='10yr real rate with core CPI', color='blue')
realrates['10yr_real_cpi'].plot(label='10yr real rate with CPI', color='green')
realrates['10yr_real_corepce'].plot(label='10yr real rate with core PCE', color='orange')
realrates['10yr_real_cpi_urban'].plot(label='10yr real rate with CPI urban', color='yellow')

plt.title('10yr real rates (with core PCE and urban CPI)')
plt.xlabel('date')
plt.ylabel('real rate (%)')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/10yr_real_rates_full.png')
# plt.show()

# real rate plot (only CPI, core CPI, PCE)

plt.figure(figsize=(10,5))

realrates['10yr_nominal'].plot(label='10yr nominal rate', color='black')

realrates['10yr_real_pce'].plot(label='10yr real rate with PCE', color='red')
realrates['10yr_real_corecpi'].plot(label='10yr real rate with core CPI', color='blue')
realrates['10yr_real_cpi'].plot(label='10yr real rate with CPI', color='green')

plt.title('10yr real rates')
plt.xlabel('date')
plt.ylabel('real rate (%)')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/10yr_real_rates.png')
# plt.show()

# inflation only plot 

plt.figure(figsize=(10,5))

inflation['pce'].plot(label='PCE', color='red')
inflation['corecpi'].plot(label='core CPI', color='blue')
inflation['cpi'].plot(label='CPI (LSEG)', color='green')
inflation['corepce'].plot(label='core PCE', color='orange')
inflation['cpi_urban'].plot(label='CPI', color='yellow')

plt.title('inflation rates')
plt.xlabel('date')
plt.ylabel('inflation rate (%)')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/inflation_rates.png')
# plt.show()

# fred real rate data

plt.figure(figsize=(10,5))

fred_real_rate = pd.read_csv('/Users/aryaman/macro-research/data/fred_real_rate.csv', index_col=0, parse_dates=True)
realrates['fred_10yr_real_rate'] = fred_real_rate['REAINTRATREARAT10Y']

realrates['fred_10yr_real_rate'].plot(label='FRED Model 10yr real rate', color='black')

realrates['10yr_real_pce'].plot(label='10yr real rate with PCE', color='red')
realrates['10yr_real_corecpi'].plot(label='10yr real rate with core CPI', color='blue')
realrates['10yr_real_cpi'].plot(label='10yr real rate with CPI', color='green')

plt.title('10yr real rates')
plt.xlabel('date')
plt.ylabel('real rate (%)')
plt.legend()
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/fred_real_rate.png')