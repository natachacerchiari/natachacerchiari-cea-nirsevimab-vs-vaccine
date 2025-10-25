"""Calculates and plots the Cost-Effectiveness Acceptability Curve (CEAC)."""

import numpy as np
import pandas as pd


def main():
    perspectives = [
        ("public", "results/psa/psa_public.csv", "results/ceac/ceac_public.csv"),
        ("societal", "results/psa/psa_societal.csv", "results/ceac/ceac_societal.csv"),
    ]

    cost_col = "incremental-cost"
    dalys_col = "incremental-dalys"

    for _, input_path, output_path in perspectives:
        df = pd.read_csv(input_path)

        # Generate CEAC data
        max_threshold = max(df[cost_col] / df[dalys_col].replace(0, np.nan))
        thresholds = np.linspace(0, max_threshold * 1.1, 100)
        probabilities = []
        for threshold in thresholds:
            prob = (df[cost_col] <= threshold * df[dalys_col]).mean()
            probabilities.append(prob)

        # Save CEAC data to CSV
        ceac_data = pd.DataFrame({"threshold": thresholds, "probability": probabilities})
        ceac_data.to_csv(output_path, index=False, encoding="utf-8", lineterminator="\n")

    print("CEAC analysis completed.")
    print(f"Results saved to {perspectives[0][2]} and {perspectives[1][2]}")


if __name__ == "__main__":
    main()
