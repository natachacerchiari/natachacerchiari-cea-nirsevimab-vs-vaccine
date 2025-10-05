"""Probabilistic Sensitivity Analysis (PSA) for the health economic model."""

import random

import numpy as np
import pandas as pd
from betapert import pert

from stat_tools.fit_distributions import (
    fit_beta,
    fit_lognormal,
    fit_lognormal_briggs,
)
from stat_tools.sampling import sample_lognormal, sample_truncated_normal
from util.constants import DAYS_IN_YEAR
from util.core import calculate_salary_loss, run_scenario
from util.data_enricher import enrich_agegroup_data, enrich_scalar_data
from util.data_loader import load_age_groups, load_agegroup_data, load_scalar_data

N = 10_000

DEFAULT_RNG = random.Random(42)
NP_RNG = np.random.default_rng(42)


def main():
    age_groups = load_age_groups()
    n_sub = len(age_groups)

    scalar_data = enrich_scalar_data(load_scalar_data())
    agegroup_data = enrich_agegroup_data(load_agegroup_data(), scalar_data)
    scalar_data = scalar_data.iloc[0]

    # Extract scalar values
    cohort = scalar_data["cohort"]
    nirsevimab_coverage = scalar_data["nirsevimab_coverage"]
    nirsevimab_min_expected_coverage = scalar_data["nirsevimab_min_expected_coverage"]
    nirsevimab_max_expected_coverage = scalar_data["nirsevimab_max_expected_coverage"]
    vaccine_coverage = scalar_data["vaccine_coverage"]
    nirsevimab_dose_cost = scalar_data["nirsevimab_dose_cost"]
    vaccine_dose_cost = scalar_data["vaccine_dose_cost"]
    severe_case_dw = scalar_data["severe_case_dw"]
    moderate_case_dw = scalar_data["moderate_case_dw"]
    severe_illness_duration_days = scalar_data["severe_illness_duration_days"]
    moderate_illness_duration_days = scalar_data["moderate_illness_duration_days"]
    discounted_yll = scalar_data["discounted_yll"]
    moderate_case_dw = scalar_data["moderate_case_dw"]
    severe_case_dw = scalar_data["severe_case_dw"]
    moderate_case_dw_ci95_lower = scalar_data["moderate_case_dw_ci95_lower"]
    moderate_case_dw_ci95_upper = scalar_data["moderate_case_dw_ci95_upper"]
    severe_case_dw_ci95_lower = scalar_data["severe_case_dw_ci95_lower"]
    severe_case_dw_ci95_upper = scalar_data["severe_case_dw_ci95_upper"]

    # Extract agegroup values as lists
    population_proportions = agegroup_data["population_proportion"].to_list()
    hosp_proportions = agegroup_data["hosp_proportion"].to_list()
    hosp_proportion_ci95_lowers = agegroup_data["hosp_proportion_ci95_lower"].to_list()
    hosp_proportion_ci95_uppers = agegroup_data["hosp_proportion_ci95_upper"].to_list()
    outpatient_proportions = agegroup_data["outpatient_proportion"].to_list()
    outpatient_proportion_ci95_lowers = agegroup_data["outpatient_proportion_ci95_lower"].to_list()
    outpatient_proportion_ci95_uppers = agegroup_data["outpatient_proportion_ci95_upper"].to_list()
    lethality_proportions = agegroup_data["lethality_proportion"].to_list()
    inpatient_costs = agegroup_data["inpatient_cost"].to_list()
    inpatient_pcr_costs = agegroup_data["inpatient_pcr_cost"].to_list()
    outpatient_ec_costs = agegroup_data["outpatient_ec_cost"].to_list()
    outpatient_pc_costs = agegroup_data["outpatient_pc_cost"].to_list()
    inpatient_transport_costs = agegroup_data["inpatient_transport_cost"].to_list()
    outpatient_transport_costs = agegroup_data["outpatient_transport_cost"].to_list()
    nirsevimab_hosp_reduction_effs = agegroup_data["nirsevimab_hosp_reduction_eff"].to_list()
    nirsevimab_hosp_reduction_eff_ci95_lowers = agegroup_data[
        "nirsevimab_hosp_reduction_eff_ci95_lower"
    ].to_list()
    nirsevimab_hosp_reduction_eff_ci95_uppers = agegroup_data[
        "nirsevimab_hosp_reduction_eff_ci95_upper"
    ].to_list()
    nirsevimab_malrti_reduction_effs = agegroup_data["nirsevimab_malrti_reduction_eff"].to_list()
    nirsevimab_malrti_reduction_eff_ci95_lowers = agegroup_data[
        "nirsevimab_malrti_reduction_eff_ci95_lower"
    ].to_list()
    nirsevimab_malrti_reduction_eff_ci95_uppers = agegroup_data[
        "nirsevimab_malrti_reduction_eff_ci95_upper"
    ].to_list()
    vaccine_hosp_reduction_effs = agegroup_data["vaccine_hosp_reduction_eff"].to_list()
    vaccine_malrti_reduction_effs = agegroup_data["vaccine_malrti_reduction_eff"].to_list()
    affected_caregivers_proportions = agegroup_data["affected_caregivers_proportion"].to_list()
    caregiver_daily_salaries = agegroup_data["caregiver_daily_salary"].to_list()

    # Fit beta parameters for DWs
    moderate_case_dw_alpha, moderate_case_dw_beta = fit_beta(
        moderate_case_dw,
        moderate_case_dw_ci95_lower,
        moderate_case_dw_ci95_upper,
    )
    severe_case_dw_alpha, severe_case_dw_beta = fit_beta(
        severe_case_dw,
        severe_case_dw_ci95_lower,
        severe_case_dw_ci95_upper,
    )

    # Fit lognormal parameters for proportions
    hosp_proportions_params = [
        fit_lognormal(
            hosp_proportions[i],
            hosp_proportion_ci95_lowers[i],
            hosp_proportion_ci95_uppers[i],
        )
        for i in range(n_sub)
    ]
    outpatient_proportions_params = [
        fit_lognormal(
            outpatient_proportions[i],
            outpatient_proportion_ci95_lowers[i],
            outpatient_proportion_ci95_uppers[i],
        )
        for i in range(n_sub)
    ]

    # Fit lognormal (Briggs) parameters for costs (25% variation)
    inpatient_costs_params = [fit_lognormal_briggs(c, 0.25) for c in inpatient_costs]
    outpatient_pc_costs_params = [fit_lognormal_briggs(c, 0.25) for c in outpatient_pc_costs]
    outpatient_ec_costs_params = [fit_lognormal_briggs(c, 0.25) for c in outpatient_ec_costs]

    # Fit lognormal (Briggs) parameters for salary loss (25% variation)
    caregiver_daily_salary_params = [
        fit_lognormal_briggs(c, 0.25) for c in caregiver_daily_salaries
    ]

    # Fit beta parameters for nirsevimab effectiveness (hospitalization reduction)
    nirsevimab_hosp_reduction_params = [None] * n_sub
    for i in range(n_sub):
        if nirsevimab_hosp_reduction_effs[i] != 0:
            alpha, beta = fit_beta(
                nirsevimab_hosp_reduction_effs[i],
                nirsevimab_hosp_reduction_eff_ci95_lowers[i],
                nirsevimab_hosp_reduction_eff_ci95_uppers[i],
            )
            nirsevimab_hosp_reduction_params[i] = (alpha, beta)

    # Fit beta parameters for nirsevimab effectiveness (malrti reduction)
    nirsevimab_malrti_reduction_params = [None] * n_sub
    for i in range(n_sub):
        if nirsevimab_malrti_reduction_effs[i] != 0:
            alpha, beta = fit_beta(
                nirsevimab_malrti_reduction_effs[i],
                nirsevimab_malrti_reduction_eff_ci95_lowers[i],
                nirsevimab_malrti_reduction_eff_ci95_uppers[i],
            )
            nirsevimab_malrti_reduction_params[i] = (alpha, beta)

    societal_results = []
    public_results = []

    for _ in range(N):
        # Draw DWs
        moderate_case_dw = DEFAULT_RNG.betavariate(moderate_case_dw_alpha, moderate_case_dw_beta)
        severe_case_dw = DEFAULT_RNG.betavariate(severe_case_dw_alpha, severe_case_dw_beta)

        # Random draws per age group
        rand_hosp_proportions = [
            sample_lognormal(1, mu, sigma, rng=DEFAULT_RNG)[0]
            for (mu, sigma) in hosp_proportions_params
        ]
        rand_outpatient_proportions = [
            sample_lognormal(1, mu, sigma, rng=DEFAULT_RNG)[0]
            for (mu, sigma) in outpatient_proportions_params
        ]
        rand_inpatient_costs = [
            sample_lognormal(1, mu, sigma, rng=DEFAULT_RNG)[0]
            for (mu, sigma) in inpatient_costs_params
        ]
        rand_outpatient_pc_costs = [
            sample_lognormal(1, mu, sigma, rng=DEFAULT_RNG)[0]
            for (mu, sigma) in outpatient_pc_costs_params
        ]
        rand_outpatient_ec_costs = [
            sample_lognormal(1, mu, sigma, rng=DEFAULT_RNG)[0]
            for (mu, sigma) in outpatient_ec_costs_params
        ]

        # Caregiver salary loss calculations
        caregiver_daily_salary_draws = [
            sample_lognormal(1, mu, sigma, rng=DEFAULT_RNG)[0]
            for (mu, sigma) in caregiver_daily_salary_params
        ]
        rand_inpatient_caregiver_salary_losses = [
            calculate_salary_loss(
                severe_illness_duration_days,
                affected_caregivers_proportions[i],
                caregiver_daily_salary_draws[i],
            )
            for i in range(n_sub)
        ]
        rand_outpatient_caregiver_salary_losses = [
            calculate_salary_loss(
                moderate_illness_duration_days,
                affected_caregivers_proportions[i],
                caregiver_daily_salary_draws[i],
            )
            for i in range(n_sub)
        ]

        # Nirsevimab effectiveness (hospitalization): beta where mean != 0, else fixed
        rand_nirsevimab_hosp_reduction_effs = []
        for i in range(n_sub):
            params = nirsevimab_hosp_reduction_params[i]
            if params is not None:
                alpha, beta = params
                sampled = DEFAULT_RNG.betavariate(alpha, beta)
                rand_nirsevimab_hosp_reduction_effs.append(sampled)
            else:
                rand_nirsevimab_hosp_reduction_effs.append(nirsevimab_hosp_reduction_effs[i])

        # Nirsevimab effectiveness (maltri): beta where mean != 0, else fixed
        rand_nirsevimab_malrti_reduction_effs = []
        for i in range(n_sub):
            params = nirsevimab_malrti_reduction_params[i]
            if params is not None:
                alpha, beta = params
                sampled = DEFAULT_RNG.betavariate(alpha, beta)
                rand_nirsevimab_malrti_reduction_effs.append(sampled)
            else:
                rand_nirsevimab_malrti_reduction_effs.append(nirsevimab_malrti_reduction_effs[i])

        # Nirsevimab coverage
        rand_nirsevimab_coverage = pert.rvs(
            mini=nirsevimab_min_expected_coverage,
            mode=nirsevimab_coverage,
            maxi=nirsevimab_max_expected_coverage,
            random_state=NP_RNG,
        )

        # Societal perspective

        result_societal_nirsevimab_dict = run_scenario(
            cohort,
            rand_nirsevimab_coverage,
            nirsevimab_dose_cost,
            severe_case_dw,
            moderate_case_dw,
            severe_illness_duration_days,
            moderate_illness_duration_days,
            DAYS_IN_YEAR,
            discounted_yll,
            population_proportions,
            rand_hosp_proportions,
            rand_outpatient_proportions,
            lethality_proportions,
            rand_inpatient_costs,
            inpatient_pcr_costs,
            rand_outpatient_ec_costs,
            rand_outpatient_pc_costs,
            inpatient_transport_costs,
            rand_inpatient_caregiver_salary_losses,
            outpatient_transport_costs,
            rand_outpatient_caregiver_salary_losses,
            rand_nirsevimab_hosp_reduction_effs,
            rand_nirsevimab_malrti_reduction_effs,
        )
        result_societal_vaccine_dict = run_scenario(
            cohort,
            vaccine_coverage,
            vaccine_dose_cost,
            severe_case_dw,
            moderate_case_dw,
            severe_illness_duration_days,
            moderate_illness_duration_days,
            DAYS_IN_YEAR,
            discounted_yll,
            population_proportions,
            rand_hosp_proportions,
            rand_outpatient_proportions,
            lethality_proportions,
            rand_inpatient_costs,
            inpatient_pcr_costs,
            rand_outpatient_ec_costs,
            rand_outpatient_pc_costs,
            inpatient_transport_costs,
            rand_inpatient_caregiver_salary_losses,
            outpatient_transport_costs,
            rand_outpatient_caregiver_salary_losses,
            vaccine_hosp_reduction_effs,
            vaccine_malrti_reduction_effs,
        )

        # Public perspective (zero salary losses)

        result_public_nirsevimab_dict = run_scenario(
            cohort,
            rand_nirsevimab_coverage,
            nirsevimab_dose_cost,
            severe_case_dw,
            moderate_case_dw,
            severe_illness_duration_days,
            moderate_illness_duration_days,
            DAYS_IN_YEAR,
            discounted_yll,
            population_proportions,
            rand_hosp_proportions,
            rand_outpatient_proportions,
            lethality_proportions,
            rand_inpatient_costs,
            inpatient_pcr_costs,
            rand_outpatient_ec_costs,
            rand_outpatient_pc_costs,
            inpatient_transport_costs,
            [0.0] * n_sub,
            outpatient_transport_costs,
            [0.0] * n_sub,
            nirsevimab_hosp_reduction_effs,
            nirsevimab_malrti_reduction_effs,
        )
        result_public_vaccine_dict = run_scenario(
            cohort,
            vaccine_coverage,
            vaccine_dose_cost,
            severe_case_dw,
            moderate_case_dw,
            severe_illness_duration_days,
            moderate_illness_duration_days,
            DAYS_IN_YEAR,
            discounted_yll,
            population_proportions,
            rand_hosp_proportions,
            rand_outpatient_proportions,
            lethality_proportions,
            rand_inpatient_costs,
            inpatient_pcr_costs,
            rand_outpatient_ec_costs,
            rand_outpatient_pc_costs,
            inpatient_transport_costs,
            [0.0] * n_sub,
            outpatient_transport_costs,
            [0.0] * n_sub,
            vaccine_hosp_reduction_effs,
            vaccine_malrti_reduction_effs,
        )

        societal_results.append(
            {
                "incremental-cost": result_societal_nirsevimab_dict["cost"]
                - result_societal_vaccine_dict["cost"],
                "incremental-dalys": result_societal_vaccine_dict["dalys"]
                - result_societal_nirsevimab_dict["dalys"],
            }
        )
        public_results.append(
            {
                "incremental-cost": result_public_nirsevimab_dict["cost"]
                - result_public_vaccine_dict["cost"],
                "incremental-dalys": result_public_vaccine_dict["dalys"]
                - result_public_nirsevimab_dict["dalys"],
            }
        )

    print("Iterations:", N)
    pd.DataFrame(public_results).to_csv("results/psa/psa_public.csv", index=False, encoding="utf-8", lineterminator="\n")
    pd.DataFrame(societal_results).to_csv("results/psa/psa_societal.csv", index=False, encoding="utf-8", lineterminator="\n")


if __name__ == "__main__":
    main()
