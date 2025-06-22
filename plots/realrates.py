import pandas as pd
import matplotlib.pyplot as plt 

# load data, rename columns for convenience 

inflation = (
    pd.read_csv('/Users/aryaman/macro-research/data/lseg_inflation.csv', parse_dates=['PeriodDate'])
      .pivot_table(index='PeriodDate', columns='EcoSeriesID', values='Series_Value')
      .sort_index()
)

inflation = inflation.rename(columns={
    135494: 'pce_index',
    156602: 'corecpi_index',
    202641: 'cpi' # already given as year-on-year percentage change 
})

yields = (
    pd.read_csv('/Users/aryaman/macro-research/data/lseg_yields.csv', parse_dates=['PeriodDate'])
      .pivot_table(index='PeriodDate', columns='EcoSeriesID', values='Series_Value')
      .sort_index()
)

yields = yields.rename(columns={200398: 'nominal10yr_yield'})

# calculate year on year inflation values (pct change from 1 year ago) and isolate relevant rates

inflation['pce'] = inflation['pce_index'].pct_change(periods=12) * 100
inflation['corecpi'] = inflation['corecpi_index'].pct_change(periods=12) * 100
inflation = inflation[['pce', 'corecpi', 'cpi']]

# resample yields to monthly (take value on the 10th of the month) 

yields = yields.resample('M').last()

# print(inflation.head(20))
print(yields.head(20))

# plt.figure(figsize=(10,5))