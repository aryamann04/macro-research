import pandas as pd 

# inflation data from FRED

fred_cpi_urban = pd.read_csv('/Users/aryaman/macro-research/data/fred_cpi_urban.csv', index_col=0, parse_dates=True)
fred_cpi_urban = fred_cpi_urban.rename(columns={'CPIAUCSL': 'fred_cpi_urban'})

# note: already percentage change from 1 year ago 
fred_core_cpi = pd.read_csv('/Users/aryaman/macro-research/data/fred_core_cpi.csv', index_col=0, parse_dates=True)
fred_core_cpi = fred_core_cpi.rename(columns={'CORESTICKM159SFRBATL': 'fred_core_cpi'})

fred_pcepi = pd.read_csv('/Users/aryaman/macro-research/data/fred_pcepi.csv', index_col=0, parse_dates=True)
fred_pcepi = fred_pcepi.rename(columns={'PCEPI': 'fred_pcepi'})

fred_core_pcepi = pd.read_csv('/Users/aryaman/macro-research/data/fred_core_pcepi.csv', index_col=0, parse_dates=True)
fred_core_pcepi = fred_core_pcepi.rename(columns={'PCEPILFE': 'fred_core_pcepi'})

fred_inflation = pd.DataFrame() 
fred_inflation.index = fred_cpi_urban.index

fred_inflation['fred_cpi_urban'] = fred_cpi_urban['fred_cpi_urban'].pct_change(periods=12) * 100
fred_inflation['fred_core_cpi'] = fred_core_cpi['fred_core_cpi']
fred_inflation['fred_pcepi'] = fred_pcepi['fred_pcepi'].pct_change(periods=12) * 100
fred_inflation['fred_core_pcepi'] = fred_core_pcepi['fred_core_pcepi'].pct_change(periods=12) * 100

fred_inflation.dropna(inplace=True)

# inflation data from LSEG

lseg_inflation = (
    pd.read_csv('/Users/aryaman/macro-research/data/lseg_inflation.csv', parse_dates=['PeriodDate'])
      .pivot_table(index='PeriodDate', columns='EcoSeriesID', values='Series_Value')
      .sort_index()
)

# already given as year-on-year percentage change 
inflation = lseg_inflation.rename(columns={202641: 'cpi'})

# isolate relevant rates
# use LSEG data for CPI; use FRED data for PCE, urban CPI, core CPI, core PCE

inflation['pce'] = fred_inflation['fred_pcepi']
inflation['cpi_urban'] = fred_inflation['fred_cpi_urban']
inflation['corecpi'] = fred_inflation['fred_core_cpi']
inflation['corepce']  = fred_inflation['fred_core_pcepi']

# NOTE: first one is LSEG data, all other are FRED data
inflation = inflation[['cpi', 'pce', 'corecpi', 'corepce', 'cpi_urban']]

# yields data
# note: monthly data is average of business days 
yields = pd.read_csv('/Users/aryaman/macro-research/data/fred_yields.csv', index_col=0, parse_dates=True)
yields = yields.rename(columns={'GS10': '10yr_yield'})