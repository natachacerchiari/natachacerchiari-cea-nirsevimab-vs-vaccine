"""Functions to fit common distributions to summary statistics."""

__all__ = ["fit_beta", "fit_normal", "fit_lognormal", "fit_lognormal_briggs"]

import math
from typing import Tuple

import numpy as np
from scipy.optimize import minimize
from scipy.stats import beta


def fit_beta(mean_target: float, lower_target: float, upper_target: float) -> Tuple[float, float]:
    """
    Fit a Beta distribution (alpha, beta) from mean and 95% CI bounds.
    Returns (alpha, beta).
    """
    if not (0 < mean_target < 1):
        raise ValueError("mean_target must be in (0,1)")
    if not (0 < lower_target < upper_target < 1):
        raise ValueError("Bounds must be within (0,1) and lower < upper")

    def objective(params: Tuple[float, float]) -> float:
        a, b = params
        if a <= 0 or b <= 0:
            return 1e12
        mean_calc = a / (a + b)
        lower_calc = beta.ppf(0.025, a, b)
        upper_calc = beta.ppf(0.975, a, b)
        return (
            50 * (mean_calc - mean_target) ** 2
            + 5 * (lower_calc - lower_target) ** 2
            + 5 * (upper_calc - upper_target) ** 2
        )

    # Method-of-moments initial guess
    sd_approx = (upper_target - lower_target) / 3.92
    var_approx = sd_approx**2
    common = mean_target * (1 - mean_target) / var_approx - 1
    a0 = mean_target * common
    b0 = (1 - mean_target) * common
    if a0 <= 0 or b0 <= 0 or math.isnan(a0) or math.isnan(b0):
        a0 = mean_target * 50
        b0 = (1 - mean_target) * 50

    res = minimize(
        objective,
        x0=[a0, b0],
        method="L-BFGS-B",
        bounds=[(1e-6, 1e6), (1e-6, 1e6)],
    )
    a_opt, b_opt = res.x
    return float(a_opt), float(b_opt)


def fit_lognormal(
    mean_target: float, lower_target: float, upper_target: float
) -> Tuple[float, float]:
    """
    Fit Lognormal parameters (mu, sigma) in log-space from mean and 95% CI bounds.
    Returns (mu, sigma).
    """
    if lower_target <= 0 or upper_target <= 0:
        raise ValueError("Bounds must be > 0 for lognormal")
    if upper_target <= lower_target:
        raise ValueError("upper_target must be greater than lower_target")
    z = 1.96
    log_l = math.log(lower_target)
    log_u = math.log(upper_target)
    sigma = (log_u - log_l) / (2 * z)
    mu = (log_l + log_u) / 2
    # Adjust mu slightly so implied mean matches mean_target (iterative one-step correction)
    implied_mean = math.exp(mu + sigma**2 / 2)
    if implied_mean > 0:
        mu += math.log(mean_target / implied_mean)
    return float(mu), float(sigma)


def fit_lognormal_briggs(central_value: float, variation: float) -> Tuple[float, float]:
    """
    Implementation based on Briggs et al. (2006).
    Assumes central_value is the median,
    and variation is the percentage variation (e.g., 0.25 for ±25%).
    Returns (mu, sigma).
    """
    if central_value <= 0:
        raise ValueError("central_value must be > 0.")
    if variation <= 0:
        raise ValueError("variation must be > 0.")

    lower_bound = central_value * (1 - variation)
    upper_bound = central_value * (1 + variation)

    mu = np.log(central_value)  # median in original scale
    sigma = (np.log(upper_bound) - np.log(lower_bound)) / (2 * 1.96)

    return float(mu), float(sigma)


def fit_normal(mean_target: float, lower_target: float, upper_target: float) -> Tuple[float, float]:
    """
    Derive Normal parameters (mean, sd) from mean and symmetric 95% CI.
    Returns (mean, sd).
    """
    if upper_target <= lower_target:
        raise ValueError("upper_target must be greater than lower_target")
    z = 1.96
    sd = (upper_target - lower_target) / (2 * z)
    return float(mean_target), float(sd)
