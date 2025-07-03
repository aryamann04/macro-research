import matplotlib.pyplot as plt
import pandas as pd 

from loader import euro_data, uk_data, japan_data, china_data
from realrates import realrates 

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




