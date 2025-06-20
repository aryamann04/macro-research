import pandas as pd 
import matplotlib.pyplot as plt

fxrates = pd.read_csv('/Users/aryaman/macro-research/data/fxrates.csv', index_col=0, parse_dates=True)
print(fxrates.head(5))
