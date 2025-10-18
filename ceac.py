"""Calculates and plots the Cost-Effectiveness Acceptability Curve (CEAC)."""

import numpy as np
import pandas as pd

COST_COL = "incremental-cost"
DALYS_COL = "incremental-dalys"

perspectives = [
    ("public", "results/psa/psa_public.csv", "results/ceac/ceac_public.csv"),
    ("societal", "results/psa/psa_societal.csv", "results/ceac/ceac_societal.csv"),
]

for _, input_path, output_path in perspectives:
    df = pd.read_csv(input_path)
    cost_mean = df[COST_COL].mean()
    dalys_mean = df[DALYS_COL].mean()

    # Calculate ICER from means
    icer = cost_mean / dalys_mean if dalys_mean != 0 else float("inf")

    # Generate CEAC data
    max_threshold = max(df[COST_COL] / df[DALYS_COL].replace(0, np.nan))
    thresholds = np.linspace(0, max_threshold * 1.1, 100)
    probabilities = []
    for threshold in thresholds:
        prob = (df[COST_COL] <= threshold * df[DALYS_COL]).mean()
        probabilities.append(prob)

    # Save CEAC data to CSV
    ceac_data = pd.DataFrame({"threshold": thresholds, "probability": probabilities})
    ceac_data.to_csv(output_path, index=False, encoding="utf-8", lineterminator="\n")

print(f"CEAC analysis completed.")
print(f"Results saved to {perspectives[0][2]} and {perspectives[1][2]}")
