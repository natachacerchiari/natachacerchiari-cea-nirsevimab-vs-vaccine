"""Generate and save sampled distributions plots based on fitted parameters."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from betapert import pert

from stat_tools.fit_distributions import (
    fit_beta,
    fit_lognormal,
    fit_lognormal_briggs,
    fit_normal,
)
from stat_tools.sampling import sample_truncated_normal
from util import (
    enrich_agegroup_data,
    enrich_scalar_data,
    load_age_groups,
    load_agegroup_data,
    load_scalar_data,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "img" / "distributions"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

N = 10_000

NP_RNG = np.random.default_rng(42)


def _save_hist(data: list[float], title: str, filename: str) -> None:
    """Save a histogram plot."""
    plt.figure(figsize=(6, 4))
    sb.histplot(data, bins=30, kde=True, color="steelblue")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename)
    plt.close()


def _save_comparative_hists(samples: list[tuple[list[float], str, str]]) -> None:
    """Save comparative histograms with consistent axes."""
    if len(samples) < 2:
        for data, title, filename in samples:
            _save_hist(data, title, filename)
        return
    all_values = np.concatenate([np.asarray(s[0]) for s in samples])
    x_min, x_max = float(all_values.min()), float(all_values.max())
    bins = np.linspace(x_min, x_max, 31)
    max_count = 0
    for data, _, _ in samples:
        counts, _ = np.histogram(data, bins=bins)
        if counts.max() > max_count:
            max_count = counts.max()
    y_max = max_count * 1.10
    for data, title, filename in samples:
        plt.figure(figsize=(6, 4))
        sb.histplot(data, bins=bins, kde=True, color="steelblue")
        plt.xlim(x_min, x_max)
        plt.ylim(0, y_max)
        plt.title(f"{title}")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / filename)
        plt.close()


# Load and enrich data
age_groups_df = load_age_groups()
scalar_data_df = enrich_scalar_data(load_scalar_data())
agegroup_data_df = enrich_agegroup_data(load_agegroup_data(), scalar_data_df)
scalar_row = scalar_data_df.iloc[0]

# Disability weights (Beta)
moderate_mean = float(scalar_row["moderate_case_dw"])
moderate_lo = float(scalar_row["moderate_case_dw_ci95_lower"])
moderate_hi = float(scalar_row["moderate_case_dw_ci95_upper"])
a_mod, b_mod = fit_beta(moderate_mean, moderate_lo, moderate_hi)
moderate_samples = NP_RNG.beta(a_mod, b_mod, N)
_save_hist(moderate_samples, "moderate_case_dw (Beta)", "moderate_case_dw_beta.png")

severe_mean = float(scalar_row["severe_case_dw"])
severe_lo = float(scalar_row["severe_case_dw_ci95_lower"])
severe_hi = float(scalar_row["severe_case_dw_ci95_upper"])
a_sev, b_sev = fit_beta(severe_mean, severe_lo, severe_hi)
severe_samples = NP_RNG.beta(a_sev, b_sev, N)
_save_hist(severe_samples, "severe_case_dw (Beta)", "severe_case_dw_beta.png")

# Epidemiologic proportions (Beta & Lognormal) per age group
for sg in agegroup_data_df.index:
    hosp_mean = float(agegroup_data_df.loc[sg, "hosp_proportion"])
    hosp_lo = float(agegroup_data_df.loc[sg, "hosp_proportion_ci95_lower"])
    hosp_hi = float(agegroup_data_df.loc[sg, "hosp_proportion_ci95_upper"])
    hosp_samples_collection = []
    try:
        a_hosp, b_hosp = fit_beta(hosp_mean, hosp_lo, hosp_hi)
        hosp_beta_samples = NP_RNG.beta(a_hosp, b_hosp, N)
        hosp_samples_collection.append(
            (
                hosp_beta_samples,
                f"hosp_proportion {sg} (Beta)",
                f"hosp_proportion_{sg}_beta.png".replace(" ", "_"),
            )
        )
    except ValueError:
        pass
    mu_hosp, sigma_hosp = fit_lognormal(hosp_mean, hosp_lo, hosp_hi)
    hosp_logn_samples = NP_RNG.lognormal(mu_hosp, sigma_hosp, N)
    hosp_samples_collection.append(
        (
            hosp_logn_samples,
            f"hosp_proportion {sg} (Lognormal)",
            f"hosp_proportion_{sg}_lognormal.png".replace(" ", "_"),
        )
    )
    _save_comparative_hists(hosp_samples_collection)

    out_mean = float(agegroup_data_df.loc[sg, "outpatient_proportion"])
    out_lo = float(agegroup_data_df.loc[sg, "outpatient_proportion_ci95_lower"])
    out_hi = float(agegroup_data_df.loc[sg, "outpatient_proportion_ci95_upper"])
    out_samples_collection = []
    try:
        a_out, b_out = fit_beta(out_mean, out_lo, out_hi)
        out_beta_samples = NP_RNG.beta(a_out, b_out, N)
        out_samples_collection.append(
            (
                out_beta_samples,
                f"outpatient_proportion {sg} (Beta)",
                f"outpatient_proportion_{sg}_beta.png".replace(" ", "_"),
            )
        )
    except ValueError:
        pass
    mu_out, sigma_out = fit_lognormal(out_mean, out_lo, out_hi)
    out_logn_samples = NP_RNG.lognormal(mu_out, sigma_out, N)
    out_samples_collection.append(
        (
            out_logn_samples,
            f"outpatient_proportion {sg} (Lognormal)",
            f"outpatient_proportion_{sg}_lognormal.png".replace(" ", "_"),
        )
    )
    _save_comparative_hists(out_samples_collection)

# Nirsevimab effectiveness (all groups with mean > 0)
for sg in agegroup_data_df.index:
    # Hospitalization reduction effectiveness
    h_mean = float(agegroup_data_df.loc[sg, "nirsevimab_hosp_reduction_eff"])
    if h_mean > 0:
        h_lo = float(agegroup_data_df.loc[sg, "nirsevimab_hosp_reduction_eff_ci95_lower"])
        h_hi = float(agegroup_data_df.loc[sg, "nirsevimab_hosp_reduction_eff_ci95_upper"])
        n_mean, n_sd = fit_normal(h_mean, h_lo, h_hi)
        hosp_norm_samples = sample_truncated_normal(N, n_mean, n_sd, 0.0, 1.0, rng=NP_RNG)
        a_h, b_h = fit_beta(h_mean, h_lo, h_hi)
        hosp_beta_samples = NP_RNG.beta(a_h, b_h, N)
        _save_comparative_hists(
            [
                (
                    hosp_norm_samples,
                    f"hosp_reduction_eff {sg} (Truncated Normal)",
                    f"hosp_reduction_eff_{sg}_normal.png".replace(" ", "_"),
                ),
                (
                    hosp_beta_samples,
                    f"hosp_reduction_eff {sg} (Beta)",
                    f"hosp_reduction_eff_{sg}_beta.png".replace(" ", "_"),
                ),
            ]
        )

    # MALRTI reduction effectiveness
    m_mean = float(agegroup_data_df.loc[sg, "nirsevimab_malrti_reduction_eff"])
    if m_mean > 0:
        m_lo = float(agegroup_data_df.loc[sg, "nirsevimab_malrti_reduction_eff_ci95_lower"])
        m_hi = float(agegroup_data_df.loc[sg, "nirsevimab_malrti_reduction_eff_ci95_upper"])
        a_m, b_m = fit_beta(m_mean, m_lo, m_hi)
        malrti_beta_samples = NP_RNG.beta(a_m, b_m, N)
        _save_hist(
            malrti_beta_samples,
            f"malrti_reduction_eff {sg} (Beta)",
            f"malrti_reduction_eff_{sg}_beta.png".replace(" ", "_"),
        )

# Nirsevimab coverage (PERT)
mini = float(scalar_row["nirsevimab_min_expected_coverage"])
mode = float(scalar_row["nirsevimab_coverage"])
maxi = float(scalar_row["nirsevimab_max_expected_coverage"])
nirsevimab_coverage_samples = [
    pert.rvs(mini=mini, mode=mode, maxi=maxi, random_state=NP_RNG) for _ in range(N)
]
_save_hist(
    nirsevimab_coverage_samples, "nirsevimab_coverage (PERT)", "nirsevimab_coverage_pert.png"
)

# Direct medical costs (inpatient per subgroup; outpatient single)
variation = 0.25
for sg in agegroup_data_df.index:
    mean_inp = float(agegroup_data_df.loc[sg, "inpatient_cost"])
    mu_inp, sigma_inp = fit_lognormal_briggs(mean_inp, variation)
    inpatient_cost_samples = NP_RNG.lognormal(mu_inp, sigma_inp, N)
    _save_hist(
        inpatient_cost_samples,
        f"inpatient_cost {sg} (Lognormal Briggs)",
        f"inpatient_cost_{sg}_lognormal.png".replace(" ", "_"),
    )

opc_mean = float(agegroup_data_df.iloc[0]["outpatient_pc_cost"])
mu_opc, sigma_opc = fit_lognormal_briggs(opc_mean, variation)
opc_samples = NP_RNG.lognormal(mu_opc, sigma_opc, N)
_save_hist(opc_samples, "outpatient_pc_cost (Lognormal Briggs)", "outpatient_pc_cost_lognormal.png")

oec_mean = float(agegroup_data_df.iloc[0]["outpatient_ec_cost"])
mu_oec, sigma_oec = fit_lognormal_briggs(oec_mean, variation)
oec_samples = NP_RNG.lognormal(mu_oec, sigma_oec, N)
_save_hist(oec_samples, "outpatient_ec_cost (Lognormal Briggs)", "outpatient_ec_cost_lognormal.png")

# Indirect costs (caregiver daily salary)
salary_mean = float(agegroup_data_df.iloc[0]["caregiver_daily_salary"])
mu_sal, sigma_sal = fit_lognormal_briggs(salary_mean, variation)
salary_samples = NP_RNG.lognormal(mu_sal, sigma_sal, N)
_save_hist(
    salary_samples,
    "caregiver_daily_salary (Lognormal Briggs)",
    "caregiver_daily_salary_lognormal.png",
)


def main():
    print("Generation complete. PNG files saved to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
