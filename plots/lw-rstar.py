import pandas as pd 
import matplotlib.pyplot as plt 

rstar_full = pd.read_csv('/Users/aryaman/macro-research/lw-model-replication/LW_2023_replication/output/LW_output.csv', index_col=0, parse_dates=True)
rstar = rstar_full.iloc[:, :6]

fig, ax1 = plt.subplots(figsize=(10, 6))

rstar['rstar'].plot(ax=ax1, color='black', linewidth=2, label='r*')
ax1.set_ylabel('r* (%)')
ax1.set_xlabel('Date')

ax2 = ax1.twinx()
rstar['output gap'].plot(ax=ax2, linestyle='--', color='orange', label='output gap')
rstar['real rate gap'].plot(ax=ax2, linestyle='--', color='green', label='real rate gap')
ax2.set_ylabel('output and real rate gaps (%)')

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper right')

plt.title('LW r* estimate and output and real rate gaps')
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/lw-rstar.png')
