import pandas as pd 
from data.fredconnect import fred 

# inflation data
def get_inflation(): 
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
    
    return inflation 

# yields data
def get_yields(): 
    # note: monthly data is average of business days 
    yields = pd.read_csv('/Users/aryaman/macro-research/data/fred_yields.csv', index_col=0, parse_dates=True)
    yields = yields.rename(columns={'GS10': '10yr_yield'})
    return yields

# EURO DATA 
def get_euro_data():
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

    return euro_data

# UK DATA
def get_uk_data():
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

    return uk_data

# JAPAN DATA
def get_japan_data(): 
    japan_inflation = pd.read_csv('/Users/aryaman/macro-research/data/japan_cpi_and_corecpi.csv', index_col=0, parse_dates=True) 
    japan_yields = pd.read_csv('/Users/aryaman/macro-research/data/fred_japan_yield.csv', index_col=0, parse_dates=True)

    japan_data = pd.DataFrame()
    japan_data.index = japan_inflation.index
    japan_data['cpi'] = japan_inflation['CPI, All Items'].pct_change(periods=12) * 100
    japan_data['core_cpi'] = japan_inflation['CPI, All items, less fresh food and energy'].pct_change(periods=12) * 100
    japan_data['10yr_yield'] = japan_yields['IRLTLT01JPM156N']
    japan_data.dropna(inplace=True)
    japan_data.index = japan_data.index.to_period('M')

    return japan_data

# CHINA DATA
def get_china_data(): 
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

    return china_data

def get_realrates():
    inflation = get_inflation()
    yields = get_yields()

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

    return realrates

def get_spots_monthly():
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

    return fxrates 


def get_spots(): 
    series = ['DEXUSEU', 'DEXUSUK', 'DEXJPUS', 'DEXCHUS']
    spot_data = {sid: fred.get_series(sid) for sid in series}
    spots = pd.DataFrame(spot_data)

    spots = spots.rename(columns={
        'DEXUSEU': 'EUR/USD',
        'DEXUSUK': 'GBP/USD',
        'DEXJPUS': 'USD/YEN',
        'DEXCHUS': 'USD/YUAN'
    })

    spots.index = pd.to_datetime(spots.index)
    spots.dropna(inplace=True)

    return spots

# for DXY spots 
def get_dxy_spots(): 
    series = ['DEXUSEU', 'DEXJPUS', 'DEXUSUK', 'DEXCAUS', 'DEXSDUS', 'DEXSZUS']
    dxy_spots = {sid: fred.get_series(sid) for sid in series}
    dxy_spots = pd.DataFrame(dxy_spots)

    dxy_spots = dxy_spots.rename(columns={
        'DEXUSEU': 'EUR/USD',
        'DEXJPUS': 'USD/YEN',
        'DEXUSUK': 'GBP/USD',
        'DEXCAUS': 'USD/CAD',
        'DEXSDUS': 'USD/SEK',
        'DEXSZUS': 'USD/CHF'
    })

    dxy_spots.index = pd.to_datetime(dxy_spots.index)
    dxy_spots.dropna(inplace=True)

    return dxy_spots

def get_overnight_interbank_rates(): 
    series = ['IRSTCI01USM156N', 'IRSTCI01EZM156N', 'IRSTCI01GBM156N', 'IRSTCI01JPM156N', 'IRSTCI01CNM156N']
    interbank_data = {sid: fred.get_series(sid) for sid in series}
    interbank_rates = pd.DataFrame(interbank_data)

    interbank_rates = interbank_rates.rename(columns={
        'IRSTCI01USM156N': 'US interbank rate',
        'IRSTCI01EZM156N': 'Euro area interbank rate',
        'IRSTCI01GBM156N': 'UK interbank rate',
        'IRSTCI01JPM156N': 'Japan interbank rate', 
        'IRSTCI01CNM156N': 'China interbank rate'
    })

    interbank_rates.index = pd.to_datetime(interbank_rates.index)
    interbank_rates.dropna(inplace=True)

    return interbank_rates

def get_3m_interbank_rates(): 
    series = ['IR3TIB01USM156N', 'IR3TIB01EZM156N', 'IR3TIB01GBM156N', 'IR3TIB01JPM156N', 'IR3TIB01CNM156N']
    interbank_data = {sid: fred.get_series(sid) for sid in series}
    interbank_rates = pd.DataFrame(interbank_data)

    interbank_rates = interbank_rates.rename(columns={
        'IR3TIB01USM156N': 'US interbank rate',
        'IR3TIB01EZM156N': 'Euro area interbank rate',
        'IR3TIB01GBM156N': 'UK interbank rate',
        'IR3TIB01JPM156N': 'Japan interbank rate', 
        'IR3TIB01CNM156N': 'China interbank rate'
    })

    interbank_rates.index = pd.to_datetime(interbank_rates.index)
    interbank_rates.dropna(inplace=True)

    return interbank_rates

# BIS data for call money 
def get_BIS_liabilities_data(): 
    urls = ["https://stats.bis.org/api/v2/data/dataflow/BIS/WS_LBS_D_PUB/1.0/Q.S.L.A.JPY.F.5J.A.5A.A.5J.N?format=csv", 
            "https://stats.bis.org/api/v2/data/dataflow/BIS/WS_LBS_D_PUB/1.0/Q.S.L.A.EUR.F.5J.A.5A.A.5J.N?format=csv",
            "https://stats.bis.org/api/v2/data/dataflow/BIS/WS_LBS_D_PUB/1.0/Q.S.L.A.GBP.F.5J.A.5A.A.5J.N?format=csv",
            ]    
    df = pd.concat([pd.read_csv(url) for url in urls])
    df = df[['L_DENOM', 'TIME_PERIOD', 'OBS_VALUE']]

    df = df.set_index(['TIME_PERIOD','L_DENOM'])['OBS_VALUE'].unstack().reset_index()
    df = df.set_index(pd.PeriodIndex(df['TIME_PERIOD'], freq='Q').to_timestamp(how='end')).sort_index()

    return df