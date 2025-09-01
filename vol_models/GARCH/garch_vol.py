import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from statsmodels.tsa.ar_model import AutoReg
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from statsmodels.stats.stattools import jarque_bera
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from arch import arch_model

def log_rets(spots: pd.Series) -> pd.Series:
    return np.log(spots).diff().dropna() * 100

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
        plt.savefig(f'/Users/aryaman/macro-research/plots/figures/GARCH/{c.replace("/", "-")}_acf_pacf.png')
        plt.show()

def ar_order(y: pd.Series, max_p: int) -> int:
    best_p, best_bic = 0, np.inf
    for p in range(1, max_p + 1):
        try:
            model = AutoReg(y, lags=p, old_names=False).fit()
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

def _fit_one(y, p_ar, vol, p, q, dist, o=None):
    kwargs = dict(mean='ARX', lags=p_ar, vol=vol, p=p, q=q, dist=dist, rescale=False)
    if o is not None:
        kwargs['o'] = o
    am = arch_model(y, **kwargs)
    res = am.fit(disp='off', cov_type='robust', tol=1e-7, update_freq=0, show_warning=False, options={'maxiter': 3000})
    return res

def fit_best_garch(y, p_ar, max_p=3, max_q=3, dists=("skewt", "t", "ged")):
    best = (None, None, None, None)
    best_bic = np.inf
    for d in dists:
        for p in range(1, max_p + 1):
            for q in range(1, max_q + 1):
                try:
                    res = _fit_one(y, p_ar, vol="GARCH", p=p, q=q, dist=d)
                    if res.bic < best_bic:
                        best_bic = res.bic
                        best = (p, q, d, res)
                except Exception:
                    continue
    if best[3] is None:
        raise RuntimeError("All GARCH fits failed for the given series.")
    return best

def fit_best_egarch(y, p_ar, max_p=3, max_o=1, max_q=3, dists=("skewt", "t", "ged")):
    best = (None, None, None, None, None)
    best_bic = np.inf
    for d in dists:
        for p in range(1, max_p + 1):
            for o in range(0, max_o + 1):
                for q in range(1, max_q + 1):
                    try:
                        res = _fit_one(y, p_ar, vol="EGARCH", p=p, q=q, dist=d, o=o)
                        if res.bic < best_bic:
                            best_bic = res.bic
                            best = (p, o, q, d, res)
                    except Exception:
                        continue
    if best[4] is None:
        raise RuntimeError("All EGARCH fits failed for the given series.")
    return best

def run_garch_and_egarch(rets: pd.DataFrame, alpha: float = 0.05, lb_lags: int = 12, max_ar: int = 1, max_garch_p: int = 3, max_garch_q: int = 3, max_egarch_p: int = 3, max_egarch_o: int = 1, max_egarch_q: int = 3, dists=("skewt", "t", "ged")):
    summaries = []
    fitted = {"GARCH": {}, "EGARCH": {}}
    diagnostics = {"GARCH": {}, "EGARCH": {}}
    for c in rets.columns:
        y = rets[c]
        n = len(y)
        _, lb_r_pval = ljung_box(y, lb_lags)
        p_ar = 0
        if lb_r_pval < alpha:
            p_ar = ar_order(y, max_ar)
        if p_ar > 0:
            mean = AutoReg(y, lags=p_ar, old_names=False, trend='c').fit()
            resid = mean.resid
        else:
            resid = y - y.mean()
        _, lb_a2_pval = ljung_box(resid ** 2, lb_lags)
        lm_pval, f_pval = engle_arch_lm(resid, max_garch_p + max_garch_q)
        gp, gq, gdist, g_res = fit_best_garch(y, p_ar, max_p=max_garch_p, max_q=max_garch_q, dists=dists)
        g_diags = get_diagnostics(g_res, lb_lags)
        fitted["GARCH"][c] = g_res
        diagnostics["GARCH"][c] = g_diags
        summaries.append({
            "pair": c,
            "model": "GARCH",
            "n": n,
            "LB(r) p-value": lb_r_pval,
            "chosen AR p (lags)": p_ar,
            "LB(a^2) p-value": lb_a2_pval,
            "ARCH LM p-value": lm_pval,
            "ARCH F p-value": f_pval,
            "p": gp, "q": gq, "o": 0,
            "dist": gdist,
            "bic": g_res.bic
        })
        ep, eo, eq, edist, e_res = fit_best_egarch(y, p_ar, max_p=max_egarch_p, max_o=max_egarch_o, max_q=max_egarch_q, dists=dists)
        e_diags = get_diagnostics(e_res, lb_lags)
        fitted["EGARCH"][c] = e_res
        diagnostics["EGARCH"][c] = e_diags
        summaries.append({
            "pair": c,
            "model": "EGARCH",
            "n": n,
            "LB(r) p-value": lb_r_pval,
            "chosen AR p (lags)": p_ar,
            "LB(a^2) p-value": lb_a2_pval,
            "ARCH LM p-value": lm_pval,
            "ARCH F p-value": f_pval,
            "p": ep, "q": eq, "o": eo,
            "dist": edist,
            "bic": e_res.bic
        })
    summary_df = pd.DataFrame(summaries).set_index(["pair", "model"]).sort_index()
    return summary_df, fitted, diagnostics

def get_garch_egarch_vols(rets: pd.DataFrame, force_new: bool = False):
    garch_path = '/Users/aryaman/macro-research/data/GARCH_vols.csv'
    egarch_path = '/Users/aryaman/macro-research/data/EGARCH_vols.csv'
    if not force_new:
        try:
            garch_df = pd.read_csv(garch_path, index_col=0, parse_dates=True)
            egarch_df = pd.read_csv(egarch_path, index_col=0, parse_dates=True)
            return {"GARCH": garch_df, "EGARCH": egarch_df}, None
        except FileNotFoundError:
            pass
    summary, fitted, diags = run_garch_and_egarch(rets)
    garch_vols = {}
    egarch_vols = {}
    for c, res in fitted["GARCH"].items():
        garch_vols[c] = pd.Series(res.conditional_volatility, index=res.resid.index)
    for c, res in fitted["EGARCH"].items():
        egarch_vols[c] = pd.Series(res.conditional_volatility, index=res.resid.index)
    garch_df = pd.concat(garch_vols, axis=1)
    egarch_df = pd.concat(egarch_vols, axis=1)
    garch_df = garch_df.reindex(rets.index).dropna()
    egarch_df = egarch_df.reindex(rets.index).dropna()
    garch_df.to_csv(garch_path)
    egarch_df.to_csv(egarch_path)
    return {"GARCH": garch_df, "EGARCH": egarch_df}, [fitted, summary, diags]

if __name__ == "__main__":
    import argparse
    from data.loader import get_spots

    arg = argparse.ArgumentParser()
    arg.add_argument("--force_new", action="store_true", help="force re-estimation of GARCH and EGARCH models")
    arg.add_argument("--validate", action="store_true", help="validate GARCH/EGARCH fits with diagnostics")
    args = arg.parse_args()

    rets = log_rets(get_spots()).truncate(before='2006-01-01')
    vols, info = get_garch_egarch_vols(rets, force_new=args.force_new)

    if info is not None and args.validate:
        fitted, summary, diags = info[0], info[1], info[2]
        print(fitted)
        print(summary)
        for pair in rets.columns: 
            print(f"{pair} GARCH:", diags["GARCH"][pair])
            print(f"{pair} EGARCH:", diags["EGARCH"][pair])
       
