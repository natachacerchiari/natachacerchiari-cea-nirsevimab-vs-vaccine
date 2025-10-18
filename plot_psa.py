"""
Generates scatter plots for PSA results from CSV files, showing incremental
DALYs averted vs. incremental costs with a WTP threshold line.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns

from util.constants import WTP

sns.set_theme(style="whitegrid")

# Read CSV files
df1 = pd.read_csv("results/psa/psa_public.csv")
df2 = pd.read_csv("results/psa/psa_societal.csv")

# Create figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# First scatter plot
if len(df1.columns) >= 2:
    x_col = df1.columns[1]
    y_col = df1.columns[0]
    sns.scatterplot(data=df1, x=x_col, y=y_col, ax=ax1)
    x_min, x_max = df1[x_col].min(), df1[x_col].max()
    ax1.plot(
        [x_min, x_max],
        [WTP * x_min, WTP * x_max],
        color="dimgray",
        linestyle="--",
        label=f"Cost-Effectiveness Threshold = {WTP:,.0f} USD/DALY",
    )
    ax1.set_title("Health System Perspective")
    ax1.set_xlabel("Incremental DALYs Averted")
    ax1.set_ylabel("Incremental Cost")
    ax1.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
    ax1.legend(loc="lower right", bbox_to_anchor=(1, -0.01))
else:
    print("First CSV doesn't have enough columns for scatter plot")

# Second scatter plot
if len(df2.columns) >= 2:
    x_col = df2.columns[1]
    y_col = df2.columns[0]
    sns.scatterplot(data=df2, x=x_col, y=y_col, ax=ax2)
    x_min, x_max = df2[x_col].min(), df2[x_col].max()
    ax2.plot(
        [x_min, x_max],
        [WTP * x_min, WTP * x_max],
        color="dimgray",
        linestyle="--",
        label=f"Cost-Effectiveness Threshold = {WTP:,.0f} USD/DALY",
    )

    ax2.set_title("Societal Perspective")
    ax2.set_xlabel("Incremental DALYs Averted")
    ax2.set_ylabel("Incremental Cost")
    ax2.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
    ax2.legend(loc="lower right", bbox_to_anchor=(1, -0.01))

else:
    print("Second CSV doesn't have enough columns for scatter plot")

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig("img/psa/psa_scatter_plots.png")
