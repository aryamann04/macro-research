import numpy as np
import pandas as pd
import scipy.stats as ss
import matplotlib.pyplot as plt

from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.stats.stattools import jarque_bera
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.gofplots import qqplot

def _std_resid_from_result(res):
    if hasattr(res, "std_resid"):  
        idx = res.resid.index
        z = pd.Series(res.std_resid, index=idx, name="z_t")
        return z

    a = pd.Series(res.resid)
    sigma = float(a.std(ddof=0))
    z = a / sigma
    z.name = "z_t"
    return z

def _dist_for_qq(res):
    nu = None
    if hasattr(res, "params"):
        try:
            nu = float(res.params.get("nu"))
        except Exception:
            nu = None
    if nu is not None and np.isfinite(nu):
        return ss.t, (nu,), f"Student-t(df={nu:,.2f})"
    return ss.norm, tuple(), "Normal"

def validate_arch_fits(fitted: dict, lb_lags=(12, 20), alpha=0.05):
    rows = []
    z_series = {}

    for name, res in fitted.items():
        z = _std_resid_from_result(res).dropna()
        z_series[name] = z

        row = {"pair": name, "n": len(z)}
        for h in lb_lags:
            lb_z   = acorr_ljungbox(z, lags=[h], return_df=True).iloc[0]
            lb_z2  = acorr_ljungbox(z**2, lags=[h], return_df=True).iloc[0]
            row[f"LB(z)@{h}_stat"] = float(lb_z["lb_stat"])
            row[f"LB(z)@{h}_p"] = float(lb_z["lb_pvalue"])
            row[f"LB(z^2)@{h}_stat"] = float(lb_z2["lb_stat"])
            row[f"LB(z^2)@{h}_p"] = float(lb_z2["lb_pvalue"])
            row[f"PASS_mean@{h}"] = row[f"LB(z)@{h}_p"]   >= alpha
            row[f"PASS_vol@{h}"] = row[f"LB(z^2)@{h}_p"] >= alpha

        jb_stat, jb_p, skew, kurt = jarque_bera(z)
        row["JB_stat"] = float(jb_stat)
        row["JB_p"] = float(jb_p)
        row["skew"] = float(skew)
        row["kurtosis"] = float(kurt) 
        rows.append(row)

    diag_df = pd.DataFrame(rows).set_index("pair")
    return diag_df, z_series

def plot_arch_diags(fitted: dict, pairs=None, lags=40):
    if pairs is None:
        pairs = list(fitted.keys())

    for name in pairs:
        res = fitted[name]
        z = _std_resid_from_result(res).dropna()
        dist, distargs, label = _dist_for_qq(res)

        fig, axes = plt.subplots(2, 2, figsize=(10, 7))
        fig.suptitle(f"{name} — standardized residual diagnostics", fontsize=12)

        # ACF z_t
        plot_acf(z, lags=lags, ax=axes[0,0])
        axes[0,0].set_title(r"ACF of $z_t$")

        # ACF z_t^2
        plot_acf(z**2, lags=lags, ax=axes[0,1])
        axes[0,1].set_title(r"ACF of $z_t^2$")

        # Q-Q
        qqplot(z, dist=dist, distargs=distargs, line="45", ax=axes[1,0])
        axes[1,0].set_title(f"QQ-plot vs {label}")

        ax = axes[1,1]
        z.plot(kind="hist", bins=60, density=True, alpha=0.35, ax=ax)
        xs = np.linspace(z.quantile(0.001), z.quantile(0.999), 400)
        ax.plot(xs, dist.pdf(xs, *distargs))
        ax.set_title(r"$z_t$ density (hist and fitted pdf)")
        plt.tight_layout()
        plt.show()