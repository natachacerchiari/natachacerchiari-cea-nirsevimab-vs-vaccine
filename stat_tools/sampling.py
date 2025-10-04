"""Sampling helper utilities."""

__all__ = ["sample_truncated_normal"]

import random
from typing import List


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
