"""
Generates tornado plots for univariate sensitivity analysis results from CSV files.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")


# Reference ICER values
REF_ICER_PHS = 255269.26
REF_ICER_SOC = 254054.75

# Shared plot variables
BAR_HEIGHT = 0.7


# Read CSV file
df_phs = pd.read_csv(
    "results/univariate/univariate.csv",
    index_col=0,
    usecols=["param_name", "icer_phs_lo", "icer_phs_hi"],
)
df_soc = pd.read_csv(
    "results/univariate/univariate.csv",
    index_col=0,
    usecols=["param_name", "icer_soc_lo", "icer_soc_hi"],
)

# Drop "caregiver_wages" index from df_phs
df_phs = df_phs.drop(index="Caregiver wages (+25% and -25%)")
empty_line = pd.DataFrame(
    {"icer_phs_lo": [REF_ICER_PHS], "icer_phs_hi": [REF_ICER_PHS]}, index=[""]
)
df_phs = pd.concat([df_phs, empty_line])

# Sort data for better visualization
df_phs["total_bar_length_phs"] = abs(df_phs["icer_phs_hi"] - df_phs["icer_phs_lo"])
df_soc["total_bar_length_soc"] = abs(df_soc["icer_soc_hi"] - df_soc["icer_soc_lo"])

# Sort data in descending order by total bar length
df_sorted_phs = df_phs.sort_values("total_bar_length_phs", ascending=True)
df_sorted_soc = df_soc.sort_values("total_bar_length_soc", ascending=True)

# Customize grid
sns.set_theme(
    style="whitegrid",
    rc={"grid.color": "0.8", "grid.linestyle": "-", "grid.linewidth": 0.5, "grid.alpha": 0.4},
)

# Customize plot fonts
plt.rcParams.update(
    {
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "figure.titlesize": 10,
    }
)

# Health system perspective tornado plot
if not df_sorted_phs.empty:
    fig1, ax1 = plt.subplots(1, 1, figsize=(8, 4))

    y_pos = np.arange(len(df_sorted_phs))

    # Plot bars for low and high values
    ax1.barh(
        y_pos,
        df_sorted_phs["icer_phs_hi"] - REF_ICER_PHS,
        left=REF_ICER_PHS,
        height=BAR_HEIGHT,
        color="darkred",
        alpha=1,
        label="High Value",
    )
    ax1.barh(
        y_pos,
        df_sorted_phs["icer_phs_lo"] - REF_ICER_PHS,
        left=REF_ICER_PHS,
        height=BAR_HEIGHT,
        color="darkblue",
        alpha=1,
        label="Low Value",
    )

    # Add reference line
    ax1.axvline(
        x=REF_ICER_PHS,
        color="dimgray",
        linestyle="--",
        linewidth=1,
        label=f"Baseline ICER = {REF_ICER_PHS:,.0f} USD/DALY",
    )

    # Customize plot
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(df_sorted_phs.index)
    ax1.set_xlabel("ICER (USD/DALY)")
    ax1.set_title("Health System Perspective - Univariate Sensitivity Analysis")
    ax1.legend(loc="lower right", fontsize=8)
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:,.0f}"))

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["bottom"].set_visible(False)
    ax1.spines["left"].set_visible(False)

    # Adjust layout and save the first plot
    plt.tight_layout()
    plt.savefig("img/univariate/univariate_tornado_phs.png", dpi=300, bbox_inches="tight")
    plt.show()


# Societal perspective tornado plot
if not df_sorted_soc.empty:
    fig2, ax2 = plt.subplots(1, 1, figsize=(8, 4))

    y_pos = np.arange(len(df_sorted_soc))

    # Plot bars for low and high values
    ax2.barh(
        y_pos,
        df_sorted_soc["icer_soc_hi"] - REF_ICER_SOC,
        left=REF_ICER_SOC,
        height=BAR_HEIGHT,
        color="darkred",
        alpha=1,
        label="High Value",
    )
    ax2.barh(
        y_pos,
        df_sorted_soc["icer_soc_lo"] - REF_ICER_SOC,
        left=REF_ICER_SOC,
        height=BAR_HEIGHT,
        color="darkblue",
        alpha=1,
        label="Low Value",
    )

    # Add reference line
    ax2.axvline(
        x=REF_ICER_SOC,
        color="dimgray",
        linestyle="--",
        linewidth=2,
        label=f"ICER baseline = {REF_ICER_SOC:,.0f} USD/DALY",
    )

    # Customize plot
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(df_sorted_soc.index)
    ax2.set_xlabel("ICER (USD/DALY)")
    ax2.set_title("Societal Perspective - Univariate Sensitivity Analysis")
    ax2.legend(loc="lower right", fontsize=8)
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:,.0f}"))

    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.spines["left"].set_visible(False)

    # Adjust layout and save the second plot
    plt.tight_layout()
    plt.savefig("img/univariate/univariate_tornado_soc.png", dpi=300, bbox_inches="tight")
    plt.show()
