import pandas as pd 
import numpy as np 

from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.diagnostic import acorr_ljungbox, het_arch
from statsmodels.tsa.stattools import jarque_bera
from arch import arch_model 

from data.loader import get_spots

def log_rets(spots: pd.Series) -> pd.Series:
    return np.log(spots).diff().dropna()

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
    stat = float(lb['lb_stat'].iloc[0])
    p_value = float(lb['lb_pvalue'].iloc[0])
    return stat, p_value

def engle_arch_lm(resids: pd.Series, m: int): 
    lm_stat, lm_pval, f_stat, f_pval = het_arch(resids, nlags=m)
    return float(lm_stat), float(lm_pval), float(f_stat), float(f_pval)

def pick_arch_order_for_joint(y: pd.Series, p_ar: int, max_m: int, dist: str = "t") -> int:
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

def diagnostics(result, lags: int):
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

def run_arch(spots: pd.DataFrame, alpha: float = 0.05, lb_lags: int = 12, max_ar: int = 5, max_arch: int = 10, dist: str = "t"): 
    spots = get_spots()
    rets = log_rets(spots)
    summary = []
    fitted = {}
    diagnostics = {}

    for c in rets.columns: 
        n = len(rets[c])

        # mean equation: test for serial dependence and pick AR(p) order
        lb_r_stat, lb_r_pval = ljung_box(rets[c], lb_lags)
        p_ar = 0 
        if lb_r_pval < alpha: 
            p_ar = ar_order(rets[c], max_ar)
        
        if p_ar > 0: 
            mean = AutoReg(rets[c], lags=p_ar, old_names=False, trend='c').fit()
            resid = mean.resid
        else: 
            resid = rets - rets.mean()
        
        # ARCH test on residuals (squared)
        lb_a2_stat, lb_a2_pval = ljung_box(resid ** 2, lb_lags)
        lm_stat, lm_pval, f_stat, f_pval = engle_arch_lm(resid, max_arch)



