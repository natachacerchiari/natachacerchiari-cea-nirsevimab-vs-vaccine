"""Sampling helper utilities."""

__all__ = ["sample_lognormal", "sample_truncated_normal"]

import math
import random
from typing import List

import numpy as np


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
    rng: np.random.Generator | None = None,
) -> List[float]:
    """
    Generate n samples from a truncated normal distribution [lo, hi] using a numpy Generator.
    """
    rng = rng or np.random.default_rng()
    if sd == 0:
        val = min(max(mean, lo), hi)
        return [val] * n
    out_parts = []
    remaining = n
    while remaining > 0:
        batch = max(remaining, 1024)
        samples = rng.normal(mean, sd, batch)
        accepted = samples[(samples >= lo) & (samples <= hi)]
        if accepted.size:
            take = min(remaining, accepted.size)
            out_parts.append(accepted[:take])
            remaining -= take
    return np.concatenate(out_parts).tolist()
