import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

from statsmodels.tsa.ar_model import AutoReg
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from statsmodels.stats.stattools import jarque_bera
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from arch import arch_model 

# x100 for better optimziation stability 
def log_rets(spots: pd.Series) -> pd.Series:
    return np.log(spots).diff().dropna() * 100

# pre-model ACF/PACF plots of log returns and squared log returns
def acf_pacf(rets: pd.DataFrame, lags: int = 40): 
    for c in rets.columns: 
        r = rets[c]
        r2 = r ** 2 

        fig, axes = plt.subplots(2, 2, figsize=(10,7))
        fig.suptitle(f"{c}: ACF/PACF of log returns and squared log returns", fontsize=12)

        plot_acf(r, lags=lags, ax=axes[0,0], zero=False)
        axes[0,0].set_title("ACF of log returns")
        plot_pacf(r, lags=lags, ax=axes[0,1], zero=False, method='ywm')
        axes[0,1].set_title("PACF of log returns")

        plot_acf(r2, lags=lags, ax=axes[1,0], zero=False)
        axes[1,0].set_title("ACF of squared log returns")
        plot_pacf(r2, lags=lags, ax=axes[1,1], zero=False, method='ywm')
        axes[1,1].set_title("PACF of squared log returns")

        for ax in axes.flat: 
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'/Users/aryaman/macro-research/plots/figures/ARCH/{c.replace("/", "-")}_acf_pacf.png')
        plt.show()

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

# try different ditributions and lags 

def select_arch(y: pd.Series, p_ar: int, max_m: int, dists=("skewt", "t", "ged")): 
    best_res, best_key = None, None
    for d in dists:
        for m in range(1, max_m + 1):
            try:
                am = arch_model(y, mean='ARX', lags=p_ar, vol='ARCH', p=m, dist=d, rescale=False)
                res = am.fit(disp='off', cov_type='robust', tol=1e-7, update_freq=0, show_warning=False, options={'maxiter': 3000})
                if (best_res is None) or (res.bic < best_res.bic):
                    best_res, best_key = res, (m, d)
            except Exception:
                continue
    if best_res is None:
        raise RuntimeError("All ARCH fits failed for the given series.")
    m_best, dist_best = best_key
    return m_best, dist_best, best_res

def run_arch(rets: pd.DataFrame, alpha: float = 0.05, lb_lags: int = 12, max_ar: int = 1, max_arch: int = 25): 
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
            m, dist, result = select_arch(rets[c], p_ar, max_arch)
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

def get_arch_vols(rets: pd.DataFrame, force_new: bool = False) -> pd.DataFrame:

    if not force_new:
        try: 
            arch_vols = pd.read_csv('/Users/aryaman/macro-research/data/ARCH_vols.csv', index_col=0, parse_dates=True)
            return arch_vols, None
        except FileNotFoundError:
            pass

    summary, fitted, diags = run_arch(rets)
    conditional_vols = {}
    for c, result in fitted.items(): 
        conditional_vols[c] = pd.Series(result.conditional_volatility, index=result.resid.index)
    
    arch_vols = pd.concat(conditional_vols, axis=1)
    arch_vols = arch_vols.reindex(rets.index).dropna()
    arch_vols.to_csv('/Users/aryaman/macro-research/data/ARCH_vols.csv')

    return arch_vols, [fitted, summary, diags]

if __name__ == "__main__":
    import argparse
    from data.loader import get_spots

    arg = argparse.ArgumentParser()
    arg.add_argument("--force_new", action="store_true", help="force re-estimation of ARCH models")
    arg.add_argument("--validate", action="store_true", help="validate ARCH fits with diagnostics")
    args = arg.parse_args()

    rets = log_rets(get_spots()).truncate(before='2006-01-01')
    arch_vols, info = get_arch_vols(rets, force_new=args.force_new)
    
    fitted, summary, diags = info[0], info[1], info[2]

    print(fitted)
    print(summary)
    print(diags)

    if fitted and args.validate: 
        from vol_models.ARCH.validate_arch import validate_arch_fits, plot_arch_diags
        diag_table, z_map = validate_arch_fits(fitted, lb_lags=(12, 20), alpha=0.05)
        print(diag_table.filter(regex="LB|JB|skew|kurt|^n$", axis=1))
        plot_arch_diags(fitted, lags=40)