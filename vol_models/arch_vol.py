import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

from statsmodels.tsa.ar_model import AutoReg
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from statsmodels.stats.stattools import jarque_bera
from arch import arch_model 

from data.loader import get_spots

# x100 for better optimziation stability 
def log_rets(spots: pd.Series) -> pd.Series:
    return np.log(spots).diff().dropna() * 100

def ar_order(y: pd.Series, max_p: int) -> int: 
    best_p, best_bic = 0, np.inf
    for p in range(1, max_p + 1):
        try: 
            model = AutoReg(y, lags=p).fit()
            if model.bic < best_bic:
                best_p, best_bic = p, model.bic
        except Exception: 
            continue

    return best_p

def ljung_box(x: pd.Series, lags: int): 
    lb = acorr_ljungbox(x, lags=[lags], return_df=True)
    return float(lb['lb_stat'].iloc[0]), float(lb['lb_pvalue'].iloc[0])

def engle_arch_lm(resids: pd.Series, m: int): 
    _, lm_pval, _, f_pval = het_arch(resids, nlags=m)
    return float(lm_pval), float(f_pval)

def arch_order(y: pd.Series, p_ar: int, max_m: int, dist: str = "t") -> int:
    best_m, best_bic = 1, np.inf
    for m in range(1, max_m + 1):
        try:
            am = arch_model(y, mean='ARX', lags=p_ar, vol='ARCH', p=m, dist=dist)
            res = am.fit(disp='off', cov_type='robust')
            if res.bic < best_bic:
                best_bic, best_m = res.bic, m
        except Exception:
            continue
    
    return best_m

def get_diagnostics(result, lags: int):
    z = pd.Series(result.std_resid, index=result.resid.index)
    stat_z, p_z = ljung_box(z, lags)
    stat_z2, p_z2 = ljung_box(z**2, lags)
    jb_stat, jb_p, skew, kurt = jarque_bera(z)

    return {
        "LB(z)_stat": stat_z, "LB(z)_p": p_z,
        "LB(z^2)_stat": stat_z2, "LB(z^2)_p": p_z2,
        "JB_stat": float(jb_stat), "JB_p": float(jb_p),
        "skew": float(skew), "kurtosis": float(kurt)
    }

def run_arch(rets: pd.DataFrame, alpha: float = 0.05, lb_lags: int = 12, max_ar: int = 5, max_arch: int = 44, dist: str = "t"): 
    summary = []
    fitted = {}
    diagnostics = {}

    for c in rets.columns: 
        n = len(rets[c])

        # mean equation: test for serial dependence and pick AR(p) order
        _, lb_r_pval = ljung_box(rets[c], lb_lags)
        p_ar = 0 
        if lb_r_pval < alpha: 
            p_ar = ar_order(rets[c], max_ar)
        
        if p_ar > 0: 
            mean = AutoReg(rets[c], lags=p_ar, old_names=False, trend='c').fit()
            resid = mean.resid
        else: 
            resid = rets[c] - rets[c].mean()
        
        # ARCH test on residuals (squared)
        _, lb_a2_pval = ljung_box(resid ** 2, lb_lags)
        lm_pval, f_pval = engle_arch_lm(resid, max_arch)

        # if ARCH effects are present, jointly estimate AR(p) and ARCH(m)
        use_arch = lb_a2_pval < alpha or lm_pval < alpha or f_pval < alpha
        if use_arch: 
            m = arch_order(rets[c], p_ar, max_arch, dist)
            am = arch_model(rets[c], mean='ARX', lags=p_ar, vol='ARCH', p=m, dist=dist)
            result = am.fit(disp='off', cov_type='robust')
        else: 
            # if no ARCH effects, just use AR(p) model 
            mean_model = AutoReg(rets[c], lags=p_ar, old_names=False, trend='c')
            result = mean_model.fit()

        # diagnostics only if ARCH was used
        diags = None
        if use_arch:
            diags = get_diagnostics(result, lb_lags)
        
        # store results 
        summary.append({
        "pair": c,
        "n": n,
        "LB(r) p-value": lb_r_pval,
        "chosen AR p (lags)": p_ar,
        "LB(a^2) p-value": lb_a2_pval,
        "ARCH LM p-value": lm_pval,
        "ARCH F p-value": f_pval,
        "ARCH used?": use_arch,
        "chosen ARCH m (lags)": m if use_arch else 0,
        "dist": dist if use_arch else "gaussian (implicit)"})

        diagnostics[c] = diags
        fitted[c] = result
    
    summary_df = pd.DataFrame(summary).set_index("pair")

    return summary_df, fitted, diagnostics

def get_arch_vols(rets: pd.DataFrame) -> pd.DataFrame:
    _, fitted, _ = run_arch(rets)
    conditional_vols = {}
    for c, result in fitted.items(): 
        conditional_vols[c] = pd.Series(result.conditional_volatility, index=result.resid.index)
    
    arch_vols = pd.concat(conditional_vols, axis=1)
    arch_vols = arch_vols.reindex(rets.index).dropna()
    arch_vols.to_csv('/Users/aryaman/macro-research/data/ARCH_vols.csv')

    return arch_vols 

# plot modelled ARCH vols

rets = log_rets(get_spots())

try: 
    arch_vols = pd.read_csv('/Users/aryaman/macro-research/data/ARCH_vols.csv', index_col=0, parse_dates=True)
except FileNotFoundError:
    arch_vols = get_arch_vols(rets)

fig, ax = plt.subplots(figsize=(12, 6))
arch_vols['EUR/USD'].plot(ax=ax, color='blue', alpha=0.7)
arch_vols['GBP/USD'].plot(ax=ax, color='green', alpha=0.7)
arch_vols['USD/YEN'].plot(ax=ax, color='red', alpha=0.7)
arch_vols['USD/YUAN'].plot(ax=ax, color='orange', alpha=0.7)

highlight_ranges = [
    ('2008-10', '2009-04'),
    ('2016-04', '2016-10'),
    ('2020-01', '2020-07'),
    ('2022-10', '2023-04'),
    ('2025-01', '2025-07')
]

for start, end in highlight_ranges:
    plt.axvspan(pd.to_datetime(start), pd.to_datetime(end), color='gray', alpha=0.2)

ax.set_title('ARCH conditional volatilities')
ax.set_ylabel('volatility (%)')
ax.set_xlabel('date')
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/ARCH_vols_daily.png')

# plot monthly annualized vol with monthly annualized ARCH vols

fxvol_by_month = rets.resample('M').std().mul(np.sqrt(252))
arch_vols_by_month = arch_vols.resample('M').mean().mul(np.sqrt(252))

plt.figure(figsize=(10, 5))

fxvol_by_month['EUR/USD'].plot(label='EUR/USD realized vol', color='blue', linestyle='--', alpha=0.7)
arch_vols_by_month['EUR/USD'].plot(label='EUR/USD ARCH vol', color='blue', linestyle='-', linewidth=1.5)

fxvol_by_month['GBP/USD'].plot(label='GBP/USD realized vol', color='green', linestyle='--', alpha=0.7)
arch_vols_by_month['GBP/USD'].plot(label='GBP/USD ARCH vol', color='green', linestyle='-', linewidth=1.5)

fxvol_by_month['USD/YEN'].plot(label='USD/YEN realized vol', color='red', linestyle='--', alpha=0.7)
arch_vols_by_month['USD/YEN'].plot(label='USD/YEN ARCH vol', color='red', linestyle='-', linewidth=1.5)

fxvol_by_month['USD/YUAN'].plot(label='USD/YUAN realized vol', color='orange', linestyle='--', alpha=0.7)
arch_vols_by_month['USD/YUAN'].plot(label='USD/YUAN ARCH vol', color='orange', linestyle='-', linewidth=1.5)

highlight_ranges = [
    ('2008-10', '2009-04'),
    ('2016-04', '2016-10'),
    ('2020-01', '2020-07'),
    ('2022-10', '2023-04'),
    ('2025-01', '2025-07')
]

for start, end in highlight_ranges:
    plt.axvspan(pd.to_datetime(start), pd.to_datetime(end), color='gray', alpha=0.2)

plt.title('monthly annualized realized volatility vs ARCH volatility')
plt.ylabel('annualized volatility (%)')
plt.xlabel('date')
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig('/Users/aryaman/macro-research/plots/figures/ARCH_vols_monthly.png')
plt.show()