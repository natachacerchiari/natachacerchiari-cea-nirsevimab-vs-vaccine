"""Sampling helper utilities."""

__all__ = ["sample_lognormal", "sample_truncated_normal"]

import math
import random
from typing import List


def sample_lognormal(
    n: int,
    mu: float,
    sigma: float,
    rng: random.Random | None = None,
) -> List[float]:
    """Generate n samples from a log-normal distribution with underlying normal(mu, sigma)."""
    r = rng if rng is not None else random
    return [math.exp(r.gauss(mu, sigma)) for _ in range(n)]


def sample_truncated_normal(
    n: int,
    mean: float,
    sd: float,
    lo: float = 0.0,
    hi: float = 1.0,
    rng: random.Random | None = None,
) -> List[float]:
    """
    Generate n samples from a truncated normal distribution [lo, hi].
    """
    r = rng if rng is not None else random
    out: List[float] = []
    for _ in range(n):
        while True:
            x = r.gauss(mean, sd)
            if lo <= x <= hi:
                out.append(x)
                break
    return out
