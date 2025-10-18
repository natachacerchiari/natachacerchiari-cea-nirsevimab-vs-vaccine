"""
Generates line plots for CEAC results from CSV files, showing probability of
cost-effectiveness vs. willingness-to-pay thresholds (USD per DALY averted).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns

from util.constants import CET

sns.set_theme(style="whitegrid")

# Read CEAC CSV files
df_public = pd.read_csv("results/ceac/ceac_public.csv")
df_societal = pd.read_csv("results/ceac/ceac_societal.csv")

# Ensure output directory exists
out_dir = Path("img/ceac")
out_dir.mkdir(parents=True, exist_ok=True)

# Create figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# First plot (public / health system perspective)
if {"threshold", "probability"}.issubset(df_public.columns):
    sns.lineplot(data=df_public, x="threshold", y="probability", ax=ax1, color="steelblue")
    ax1.axvline(
        CET,
        color="dimgray",
        linestyle="--",
        label=f"Cost-Effectiveness Threshold = {CET:,.0f} USD/DALY",
    )
    ax1.set_title("Health System Perspective")
    ax1.set_xlabel("Cost-Effectiveness Threshold (USD per DALY averted)")
    ax1.set_ylabel("Probability Cost-Effective")
    ax1.set_ylim(0, 1)
    ax1.yaxis.set_major_locator(plt.MaxNLocator(6))
    ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0%}"))
    ax1.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
    ax1.legend()
else:
    print("Public CEAC CSV missing required columns")

# Second plot (societal perspective)
if {"threshold", "probability"}.issubset(df_societal.columns):
    sns.lineplot(data=df_societal, x="threshold", y="probability", ax=ax2, color="steelblue")
    # Cost-Effectiveness Threshold vertical line
    ax2.axvline(
        CET,
        color="dimgray",
        linestyle="--",
        label=f"Cost-Effectiveness Threshold = {CET:,.0f} USD/DALY",
    )
    ax2.set_title("Societal Perspective")
    ax2.set_xlabel("Cost-Effectiveness Threshold (USD per DALY averted)")
    ax2.set_ylabel("Probability Cost-Effective")
    ax2.set_ylim(0, 1)
    ax2.yaxis.set_major_locator(plt.MaxNLocator(6))
    ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0%}"))
    ax2.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
    ax2.legend()
else:
    print("Societal CEAC CSV missing required columns")

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig(out_dir / "ceac_plots.png")
