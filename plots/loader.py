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

# EURO DATA 

euro_hicp = pd.read_csv('/Users/aryaman/macro-research/data/ecb_hicp.csv', index_col=0, parse_dates=True)
euro_core_hicp = pd.read_csv('/Users/aryaman/macro-research/data/ecb_core_hicp.csv', index_col=0, parse_dates=True)
euro_yields = pd.read_csv('/Users/aryaman/macro-research/data/ecb_yield.csv', index_col=0, parse_dates=True)

euro_data = pd.DataFrame()
euro_data.index = euro_hicp.index
euro_data['hicp'] = euro_hicp['HICP - Overall index (ICP.M.U2.N.000000.4.ANR)']
euro_data['core_hicp'] = euro_core_hicp['HICP - All-items excluding energy and food (ICP.M.U2.N.XEF000.4.ANR)']
euro_data['10yr_yield'] = euro_yields['Long-term interest rate for convergence purposes - 10 years maturity, denominated in Euro - Euro area 20 (fixed composition) as of 1 January 2023 (IRS.M.I9.L.L40.CI.0000.EUR.N.Z)']
euro_data.dropna(inplace=True)
euro_data.index = euro_data.index.to_period('M')

# UK DATA

uk_cpi = pd.read_csv('/Users/aryaman/macro-research/data/fred_uk_cpi.csv', index_col=0, parse_dates=True)
uk_core_cpi = pd.read_csv('/Users/aryaman/macro-research/data/fred_uk_core_cpi.csv', index_col=0, parse_dates=True)
uk_yields = pd.read_csv('/Users/aryaman/macro-research/data/boe_yield.csv', index_col=0, parse_dates=True)
uk_yields = uk_yields.sort_index().to_period('M')
uk_yields.index = uk_yields.index.to_timestamp()

uk_data = pd.DataFrame()
uk_data.index = uk_cpi.index
uk_data['cpi'] = uk_cpi['GBRCPIALLMINMEI'].pct_change(periods=12) * 100
uk_data['core_cpi'] = uk_core_cpi['GBRCPICORMINMEI'].pct_change(periods=12) * 100
uk_data['10yr_yield'] = uk_yields['Monthly average yield from British Government Securities, 10 year Nominal Par Yield              [a] [b] [c]             IUMAMNPY']

uk_data.dropna(inplace=True)
uk_data.index = uk_data.index.to_period('M')

# JAPAN DATA

japan_inflation = pd.read_csv('/Users/aryaman/macro-research/data/japan_cpi_and_corecpi.csv', index_col=0, parse_dates=True) 
japan_yields = pd.read_csv('/Users/aryaman/macro-research/data/fred_japan_yield.csv', index_col=0, parse_dates=True)

japan_data = pd.DataFrame()
japan_data.index = japan_inflation.index
japan_data['cpi'] = japan_inflation['CPI, All Items'].pct_change(periods=12) * 100
japan_data['core_cpi'] = japan_inflation['CPI, All items, less fresh food and energy'].pct_change(periods=12) * 100
japan_data['10yr_yield'] = japan_yields['IRLTLT01JPM156N']
japan_data.dropna(inplace=True)
japan_data.index = japan_data.index.to_period('M')

# CHINA DATA

china_inflation = pd.read_csv('/Users/aryaman/macro-research/data/oecd_china_inflation.csv')
china_inflation.drop(['Reference area', 'STRUCTURE', 'STRUCTURE_ID', 'STRUCTURE_NAME', 'ACTION', 'REF_AREA', 'FREQ', 'Frequency of observation', 'METHODOLOGY',
       'Methodology', 'MEASURE', 'Measure', 'UNIT_MEASURE',
       'EXPENDITURE', 'Expenditure', 'ADJUSTMENT', 'Adjustment',
       'TRANSFORMATION', 'Transformation',
       'OBS_STATUS', 'Observation status',
       'UNIT_MULT', 'Unit multiplier', 'BASE_PER', 'Base period', 'DURABILITY',
       'Durability', 'DECIMALS', 'Decimals', 'Time period', 'Observation value'], axis=1, inplace=True)
china_inflation = china_inflation.loc[china_inflation['Unit of measure'] == 'Index']
china_inflation.drop(['Unit of measure'], axis=1, inplace=True)
china_inflation.sort_values(by=['TIME_PERIOD'], inplace=True)
china_inflation.set_index('TIME_PERIOD', inplace=True)

china_inflation = china_inflation.rename(columns={'OBS_VALUE': 'cpi'})
china_inflation.index = pd.to_datetime(china_inflation.index)
china_inflation.index = china_inflation.index.to_period('M')
china_inflation = china_inflation['cpi'].pct_change(periods=12) * 100
china_inflation.dropna(inplace=True)
china_inflation = china_inflation.truncate(before='2006-03-01')

china_yields = pd.read_csv('/Users/aryaman/macro-research/data/chinabond_yield.csv', index_col=0, parse_dates=True)
china_yields = china_yields.rename(columns={'Yield': '10yr_yield'})
china_yields = china_yields['10yr_yield'].resample('M').mean()
china_yields.index = china_yields.index.to_period('M')

china_data = pd.DataFrame()
china_data.index = china_inflation.index
china_data['cpi'] = china_inflation
china_data['10yr_yield'] = china_yields
print(china_data.head())