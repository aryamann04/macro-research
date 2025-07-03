import matplotlib.pyplot as plt
import pandas as pd 

from loader import euro_data, uk_data, japan_data, china_data

euro_data['10yr_real_hicp'] = euro_data['10yr_yield'] - euro_data['hicp']   
euro_data['10yr_real_core_hicp'] = euro_data['10yr_yield'] - euro_data['core_hicp']

uk_data['10yr_real_cpi'] = uk_data['10yr_yield'] - uk_data['cpi']
uk_data['10yr_real_core_cpi'] = uk_data['10yr_yield'] - uk_data['core_cpi']
japan_data['10yr_real_cpi'] = japan_data['10yr_yield'] - japan_data['cpi']

# no core cpi data available for china 
china_data['10yr_real_cpi'] = china_data['10yr_yield'] - china_data['cpi']



