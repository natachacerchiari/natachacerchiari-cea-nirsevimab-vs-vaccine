import pandas as pd

from util.constants import DAYS_IN_YEAR
from util.core import run_scenario
from util.data_enricher import enrich_agegroup_data, enrich_scalar_data
from util.data_loader import load_age_groups, load_agegroup_data, load_scalar_data


def run_univariate(
    param_name,
    n_coverage=None,
    hosp_proportions=None,
    outpatient_proportions=None,
    inpatient_costs_factors=None,
    outpatient_ec_costs_factors=None,
    outpatient_pc_costs_factors=None,
    inpatient_caregiver_salary_losses_factors=None,
    outpatient_caregiver_salary_losses_factors=None,
    n_hosp_reduction_effs=None,
    n_malrti_reduction_effs=None,
):
    age_groups = load_age_groups()
    scalar_data = enrich_scalar_data(load_scalar_data())
    agegroup_data = enrich_agegroup_data(load_agegroup_data(), scalar_data)
    scalar_data = scalar_data.iloc[0]

    # Societal perspective (lower CI limit)

    nirsevimab_result = run_scenario(
        cohort=scalar_data["cohort"],
        coverage=n_coverage[0] if n_coverage is not None else scalar_data["nirsevimab_coverage"],
        intervention_dose_cost=scalar_data["nirsevimab_dose_cost"],
        severe_case_dw=scalar_data["severe_case_dw"],
        moderate_case_dw=scalar_data["moderate_case_dw"],
        severe_illness_duration_days=scalar_data["severe_illness_duration_days"],
        moderate_illness_duration_days=scalar_data["moderate_illness_duration_days"],
        days_in_year=DAYS_IN_YEAR,
        discounted_yll=scalar_data["discounted_yll"],
        population_proportions=agegroup_data["population_proportion"].to_list(),
        hosp_proportions=(
            hosp_proportions[0]
            if hosp_proportions is not None
            else agegroup_data["hosp_proportion"].to_list()
        ),
        outpatient_proportions=(
            outpatient_proportions[0]
            if outpatient_proportions is not None
            else agegroup_data["outpatient_proportion"].to_list()
        ),
        lethality_proportions=agegroup_data["lethality_proportion"].to_list(),
        inpatient_costs=(
            (agegroup_data["inpatient_cost"] * inpatient_costs_factors[0]).to_list()
            if inpatient_costs_factors is not None
            else agegroup_data["inpatient_cost"].to_list()
        ),
        inpatient_pcr_costs=agegroup_data["inpatient_pcr_cost"].to_list(),
        outpatient_ec_costs=(
            (agegroup_data["outpatient_ec_cost"] * outpatient_ec_costs_factors[0]).to_list()
            if outpatient_ec_costs_factors is not None
            else agegroup_data["outpatient_ec_cost"].to_list()
        ),
        outpatient_pc_costs=(
            (agegroup_data["outpatient_pc_cost"] * outpatient_pc_costs_factors[0]).to_list()
            if outpatient_pc_costs_factors is not None
            else agegroup_data["outpatient_pc_cost"].to_list()
        ),
        inpatient_transport_costs=agegroup_data["inpatient_transport_cost"].to_list(),
        inpatient_caregiver_salary_losses=(
            (
                agegroup_data["inpatient_caregiver_salary_loss"]
                * inpatient_caregiver_salary_losses_factors[0]
            ).to_list()
            if inpatient_caregiver_salary_losses_factors is not None
            else agegroup_data["inpatient_caregiver_salary_loss"].to_list()
        ),
        outpatient_transport_costs=agegroup_data["outpatient_transport_cost"].to_list(),
        outpatient_caregiver_salary_losses=(
            (
                agegroup_data["outpatient_caregiver_salary_loss"]
                * outpatient_caregiver_salary_losses_factors[0]
            ).to_list()
            if outpatient_caregiver_salary_losses_factors is not None
            else agegroup_data["outpatient_caregiver_salary_loss"].to_list()
        ),
        hosp_reduction_effs=(
            n_hosp_reduction_effs[0]
            if n_hosp_reduction_effs is not None
            else agegroup_data["nirsevimab_hosp_reduction_eff"].to_list()
        ),
        malrti_reduction_effs=(
            n_malrti_reduction_effs[0]
            if n_malrti_reduction_effs is not None
            else agegroup_data["nirsevimab_malrti_reduction_eff"].to_list()
        ),
    )

    vaccine_result = run_scenario(
        cohort=scalar_data["cohort"],
        coverage=scalar_data["vaccine_coverage"],
        intervention_dose_cost=scalar_data["vaccine_dose_cost"],
        severe_case_dw=scalar_data["severe_case_dw"],
        moderate_case_dw=scalar_data["moderate_case_dw"],
        severe_illness_duration_days=scalar_data["severe_illness_duration_days"],
        moderate_illness_duration_days=scalar_data["moderate_illness_duration_days"],
        days_in_year=DAYS_IN_YEAR,
        discounted_yll=scalar_data["discounted_yll"],
        population_proportions=agegroup_data["population_proportion"].to_list(),
        hosp_proportions=(
            hosp_proportions[0]
            if hosp_proportions is not None
            else agegroup_data["hosp_proportion"].to_list()
        ),
        outpatient_proportions=(
            outpatient_proportions[0]
            if outpatient_proportions is not None
            else agegroup_data["outpatient_proportion"].to_list()
        ),
        lethality_proportions=agegroup_data["lethality_proportion"].to_list(),
        inpatient_costs=(
            (agegroup_data["inpatient_cost"] * inpatient_costs_factors[0]).to_list()
            if inpatient_costs_factors is not None
            else agegroup_data["inpatient_cost"].to_list()
        ),
        inpatient_pcr_costs=agegroup_data["inpatient_pcr_cost"].to_list(),
        outpatient_ec_costs=(
            (agegroup_data["outpatient_ec_cost"] * outpatient_ec_costs_factors[0]).to_list()
            if outpatient_ec_costs_factors is not None
            else agegroup_data["outpatient_ec_cost"].to_list()
        ),
        outpatient_pc_costs=(
            (agegroup_data["outpatient_pc_cost"] * outpatient_pc_costs_factors[0]).to_list()
            if outpatient_pc_costs_factors is not None
            else agegroup_data["outpatient_pc_cost"].to_list()
        ),
        inpatient_transport_costs=agegroup_data["inpatient_transport_cost"].to_list(),
        inpatient_caregiver_salary_losses=(
            (
                agegroup_data["inpatient_caregiver_salary_loss"]
                * inpatient_caregiver_salary_losses_factors[0]
            ).to_list()
            if inpatient_caregiver_salary_losses_factors is not None
            else agegroup_data["inpatient_caregiver_salary_loss"].to_list()
        ),
        outpatient_transport_costs=agegroup_data["outpatient_transport_cost"].to_list(),
        outpatient_caregiver_salary_losses=(
            (
                agegroup_data["outpatient_caregiver_salary_loss"]
                * outpatient_caregiver_salary_losses_factors[0]
            ).to_list()
            if outpatient_caregiver_salary_losses_factors is not None
            else agegroup_data["outpatient_caregiver_salary_loss"].to_list()
        ),
        hosp_reduction_effs=agegroup_data["vaccine_hosp_reduction_eff"].to_list(),
        malrti_reduction_effs=agegroup_data["vaccine_malrti_reduction_eff"].to_list(),
    )

    icer_soc_lo = (nirsevimab_result["cost"] - vaccine_result["cost"]) / (
        vaccine_result["dalys"] - nirsevimab_result["dalys"]
    )

    # Societal perspective (upper CI limit)

    nirsevimab_result = run_scenario(
        cohort=scalar_data["cohort"],
        coverage=n_coverage[1] if n_coverage is not None else scalar_data["nirsevimab_coverage"],
        intervention_dose_cost=scalar_data["nirsevimab_dose_cost"],
        severe_case_dw=scalar_data["severe_case_dw"],
        moderate_case_dw=scalar_data["moderate_case_dw"],
        severe_illness_duration_days=scalar_data["severe_illness_duration_days"],
        moderate_illness_duration_days=scalar_data["moderate_illness_duration_days"],
        days_in_year=DAYS_IN_YEAR,
        discounted_yll=scalar_data["discounted_yll"],
        population_proportions=agegroup_data["population_proportion"].to_list(),
        hosp_proportions=(
            hosp_proportions[1]
            if hosp_proportions is not None
            else agegroup_data["hosp_proportion"].to_list()
        ),
        outpatient_proportions=(
            outpatient_proportions[1]
            if outpatient_proportions is not None
            else agegroup_data["outpatient_proportion"].to_list()
        ),
        lethality_proportions=agegroup_data["lethality_proportion"].to_list(),
        inpatient_costs=(
            (agegroup_data["inpatient_cost"] * inpatient_costs_factors[1]).to_list()
            if inpatient_costs_factors is not None
            else agegroup_data["inpatient_cost"].to_list()
        ),
        inpatient_pcr_costs=agegroup_data["inpatient_pcr_cost"].to_list(),
        outpatient_ec_costs=(
            (agegroup_data["outpatient_ec_cost"] * outpatient_ec_costs_factors[1]).to_list()
            if outpatient_ec_costs_factors is not None
            else agegroup_data["outpatient_ec_cost"].to_list()
        ),
        outpatient_pc_costs=(
            (agegroup_data["outpatient_pc_cost"] * outpatient_pc_costs_factors[1]).to_list()
            if outpatient_pc_costs_factors is not None
            else agegroup_data["outpatient_pc_cost"].to_list()
        ),
        inpatient_transport_costs=agegroup_data["inpatient_transport_cost"].to_list(),
        inpatient_caregiver_salary_losses=(
            (
                agegroup_data["inpatient_caregiver_salary_loss"]
                * inpatient_caregiver_salary_losses_factors[1]
            ).to_list()
            if inpatient_caregiver_salary_losses_factors is not None
            else agegroup_data["inpatient_caregiver_salary_loss"].to_list()
        ),
        outpatient_transport_costs=agegroup_data["outpatient_transport_cost"].to_list(),
        outpatient_caregiver_salary_losses=(
            (
                agegroup_data["outpatient_caregiver_salary_loss"]
                * outpatient_caregiver_salary_losses_factors[1]
            ).to_list()
            if outpatient_caregiver_salary_losses_factors is not None
            else agegroup_data["outpatient_caregiver_salary_loss"].to_list()
        ),
        hosp_reduction_effs=(
            n_hosp_reduction_effs[1]
            if n_hosp_reduction_effs is not None
            else agegroup_data["nirsevimab_hosp_reduction_eff"].to_list()
        ),
        malrti_reduction_effs=(
            n_malrti_reduction_effs[1]
            if n_malrti_reduction_effs is not None
            else agegroup_data["nirsevimab_malrti_reduction_eff"].to_list()
        ),
    )

    vaccine_result = run_scenario(
        cohort=scalar_data["cohort"],
        coverage=scalar_data["vaccine_coverage"],
        intervention_dose_cost=scalar_data["vaccine_dose_cost"],
        severe_case_dw=scalar_data["severe_case_dw"],
        moderate_case_dw=scalar_data["moderate_case_dw"],
        severe_illness_duration_days=scalar_data["severe_illness_duration_days"],
        moderate_illness_duration_days=scalar_data["moderate_illness_duration_days"],
        days_in_year=DAYS_IN_YEAR,
        discounted_yll=scalar_data["discounted_yll"],
        population_proportions=agegroup_data["population_proportion"].to_list(),
        hosp_proportions=(
            hosp_proportions[1]
            if hosp_proportions is not None
            else agegroup_data["hosp_proportion"].to_list()
        ),
        outpatient_proportions=(
            outpatient_proportions[1]
            if outpatient_proportions is not None
            else agegroup_data["outpatient_proportion"].to_list()
        ),
        lethality_proportions=agegroup_data["lethality_proportion"].to_list(),
        inpatient_costs=(
            (agegroup_data["inpatient_cost"] * inpatient_costs_factors[1]).to_list()
            if inpatient_costs_factors is not None
            else agegroup_data["inpatient_cost"].to_list()
        ),
        inpatient_pcr_costs=agegroup_data["inpatient_pcr_cost"].to_list(),
        outpatient_ec_costs=(
            (agegroup_data["outpatient_ec_cost"] * outpatient_ec_costs_factors[1]).to_list()
            if outpatient_ec_costs_factors is not None
            else agegroup_data["outpatient_ec_cost"].to_list()
        ),
        outpatient_pc_costs=(
            (agegroup_data["outpatient_pc_cost"] * outpatient_pc_costs_factors[1]).to_list()
            if outpatient_pc_costs_factors is not None
            else agegroup_data["outpatient_pc_cost"].to_list()
        ),
        inpatient_transport_costs=agegroup_data["inpatient_transport_cost"].to_list(),
        inpatient_caregiver_salary_losses=(
            (
                agegroup_data["inpatient_caregiver_salary_loss"]
                * inpatient_caregiver_salary_losses_factors[1]
            ).to_list()
            if inpatient_caregiver_salary_losses_factors is not None
            else agegroup_data["inpatient_caregiver_salary_loss"].to_list()
        ),
        outpatient_transport_costs=agegroup_data["outpatient_transport_cost"].to_list(),
        outpatient_caregiver_salary_losses=(
            (
                agegroup_data["outpatient_caregiver_salary_loss"]
                * outpatient_caregiver_salary_losses_factors[1]
            ).to_list()
            if outpatient_caregiver_salary_losses_factors is not None
            else agegroup_data["outpatient_caregiver_salary_loss"].to_list()
        ),
        hosp_reduction_effs=agegroup_data["vaccine_hosp_reduction_eff"].to_list(),
        malrti_reduction_effs=agegroup_data["vaccine_malrti_reduction_eff"].to_list(),
    )

    icer_soc_hi = (nirsevimab_result["cost"] - vaccine_result["cost"]) / (
        vaccine_result["dalys"] - nirsevimab_result["dalys"]
    )

    # Public health system perspective (lower CI limit)

    nirsevimab_result = run_scenario(
        cohort=scalar_data["cohort"],
        coverage=n_coverage[0] if n_coverage is not None else scalar_data["nirsevimab_coverage"],
        intervention_dose_cost=scalar_data["nirsevimab_dose_cost"],
        severe_case_dw=scalar_data["severe_case_dw"],
        moderate_case_dw=scalar_data["moderate_case_dw"],
        severe_illness_duration_days=scalar_data["severe_illness_duration_days"],
        moderate_illness_duration_days=scalar_data["moderate_illness_duration_days"],
        days_in_year=DAYS_IN_YEAR,
        discounted_yll=scalar_data["discounted_yll"],
        population_proportions=agegroup_data["population_proportion"].to_list(),
        hosp_proportions=(
            hosp_proportions[0]
            if hosp_proportions is not None
            else agegroup_data["hosp_proportion"].to_list()
        ),
        outpatient_proportions=(
            outpatient_proportions[0]
            if outpatient_proportions is not None
            else agegroup_data["outpatient_proportion"].to_list()
        ),
        lethality_proportions=agegroup_data["lethality_proportion"].to_list(),
        inpatient_costs=(
            (agegroup_data["inpatient_cost"] * inpatient_costs_factors[0]).to_list()
            if inpatient_costs_factors is not None
            else agegroup_data["inpatient_cost"].to_list()
        ),
        inpatient_pcr_costs=agegroup_data["inpatient_pcr_cost"].to_list(),
        outpatient_ec_costs=(
            (agegroup_data["outpatient_ec_cost"] * outpatient_ec_costs_factors[0]).to_list()
            if outpatient_ec_costs_factors is not None
            else agegroup_data["outpatient_ec_cost"].to_list()
        ),
        outpatient_pc_costs=(
            (agegroup_data["outpatient_pc_cost"] * outpatient_pc_costs_factors[0]).to_list()
            if outpatient_pc_costs_factors is not None
            else agegroup_data["outpatient_pc_cost"].to_list()
        ),
        inpatient_transport_costs=[0.0] * len(age_groups),
        inpatient_caregiver_salary_losses=[0.0] * len(age_groups),
        outpatient_transport_costs=[0.0] * len(age_groups),
        outpatient_caregiver_salary_losses=[0.0] * len(age_groups),
        hosp_reduction_effs=(
            n_hosp_reduction_effs[0]
            if n_hosp_reduction_effs is not None
            else agegroup_data["nirsevimab_hosp_reduction_eff"].to_list()
        ),
        malrti_reduction_effs=(
            n_malrti_reduction_effs[0]
            if n_malrti_reduction_effs is not None
            else agegroup_data["nirsevimab_malrti_reduction_eff"].to_list()
        ),
    )

    vaccine_result = run_scenario(
        cohort=scalar_data["cohort"],
        coverage=scalar_data["vaccine_coverage"],
        intervention_dose_cost=scalar_data["vaccine_dose_cost"],
        severe_case_dw=scalar_data["severe_case_dw"],
        moderate_case_dw=scalar_data["moderate_case_dw"],
        severe_illness_duration_days=scalar_data["severe_illness_duration_days"],
        moderate_illness_duration_days=scalar_data["moderate_illness_duration_days"],
        days_in_year=DAYS_IN_YEAR,
        discounted_yll=scalar_data["discounted_yll"],
        population_proportions=agegroup_data["population_proportion"].to_list(),
        hosp_proportions=(
            hosp_proportions[0]
            if hosp_proportions is not None
            else agegroup_data["hosp_proportion"].to_list()
        ),
        outpatient_proportions=(
            outpatient_proportions[0]
            if outpatient_proportions is not None
            else agegroup_data["outpatient_proportion"].to_list()
        ),
        lethality_proportions=agegroup_data["lethality_proportion"].to_list(),
        inpatient_costs=(
            (agegroup_data["inpatient_cost"] * inpatient_costs_factors[0]).to_list()
            if inpatient_costs_factors is not None
            else agegroup_data["inpatient_cost"].to_list()
        ),
        inpatient_pcr_costs=agegroup_data["inpatient_pcr_cost"].to_list(),
        outpatient_ec_costs=(
            (agegroup_data["outpatient_ec_cost"] * outpatient_ec_costs_factors[0]).to_list()
            if outpatient_ec_costs_factors is not None
            else agegroup_data["outpatient_ec_cost"].to_list()
        ),
        outpatient_pc_costs=(
            (agegroup_data["outpatient_pc_cost"] * outpatient_pc_costs_factors[0]).to_list()
            if outpatient_pc_costs_factors is not None
            else agegroup_data["outpatient_pc_cost"].to_list()
        ),
        inpatient_transport_costs=[0.0] * len(age_groups),
        inpatient_caregiver_salary_losses=[0.0] * len(age_groups),
        outpatient_transport_costs=[0.0] * len(age_groups),
        outpatient_caregiver_salary_losses=[0.0] * len(age_groups),
        hosp_reduction_effs=agegroup_data["vaccine_hosp_reduction_eff"].to_list(),
        malrti_reduction_effs=agegroup_data["vaccine_malrti_reduction_eff"].to_list(),
    )

    icer_phs_lo = (nirsevimab_result["cost"] - vaccine_result["cost"]) / (
        vaccine_result["dalys"] - nirsevimab_result["dalys"]
    )

    # Public health system perspective (upper CI limit)

    nirsevimab_result = run_scenario(
        cohort=scalar_data["cohort"],
        coverage=n_coverage[1] if n_coverage is not None else scalar_data["nirsevimab_coverage"],
        intervention_dose_cost=scalar_data["nirsevimab_dose_cost"],
        severe_case_dw=scalar_data["severe_case_dw"],
        moderate_case_dw=scalar_data["moderate_case_dw"],
        severe_illness_duration_days=scalar_data["severe_illness_duration_days"],
        moderate_illness_duration_days=scalar_data["moderate_illness_duration_days"],
        days_in_year=DAYS_IN_YEAR,
        discounted_yll=scalar_data["discounted_yll"],
        population_proportions=agegroup_data["population_proportion"].to_list(),
        hosp_proportions=(
            hosp_proportions[1]
            if hosp_proportions is not None
            else agegroup_data["hosp_proportion"].to_list()
        ),
        outpatient_proportions=(
            outpatient_proportions[1]
            if outpatient_proportions is not None
            else agegroup_data["outpatient_proportion"].to_list()
        ),
        lethality_proportions=agegroup_data["lethality_proportion"].to_list(),
        inpatient_costs=(
            (agegroup_data["inpatient_cost"] * inpatient_costs_factors[1]).to_list()
            if inpatient_costs_factors is not None
            else agegroup_data["inpatient_cost"].to_list()
        ),
        inpatient_pcr_costs=agegroup_data["inpatient_pcr_cost"].to_list(),
        outpatient_ec_costs=(
            (agegroup_data["outpatient_ec_cost"] * outpatient_ec_costs_factors[1]).to_list()
            if outpatient_ec_costs_factors is not None
            else agegroup_data["outpatient_ec_cost"].to_list()
        ),
        outpatient_pc_costs=(
            (agegroup_data["outpatient_pc_cost"] * outpatient_pc_costs_factors[1]).to_list()
            if outpatient_pc_costs_factors is not None
            else agegroup_data["outpatient_pc_cost"].to_list()
        ),
        inpatient_transport_costs=[0.0] * len(age_groups),
        inpatient_caregiver_salary_losses=[0.0] * len(age_groups),
        outpatient_transport_costs=[0.0] * len(age_groups),
        outpatient_caregiver_salary_losses=[0.0] * len(age_groups),
        hosp_reduction_effs=(
            n_hosp_reduction_effs[1]
            if n_hosp_reduction_effs is not None
            else agegroup_data["nirsevimab_hosp_reduction_eff"].to_list()
        ),
        malrti_reduction_effs=(
            n_malrti_reduction_effs[1]
            if n_malrti_reduction_effs is not None
            else agegroup_data["nirsevimab_malrti_reduction_eff"].to_list()
        ),
    )

    vaccine_result = run_scenario(
        cohort=scalar_data["cohort"],
        coverage=scalar_data["vaccine_coverage"],
        intervention_dose_cost=scalar_data["vaccine_dose_cost"],
        severe_case_dw=scalar_data["severe_case_dw"],
        moderate_case_dw=scalar_data["moderate_case_dw"],
        severe_illness_duration_days=scalar_data["severe_illness_duration_days"],
        moderate_illness_duration_days=scalar_data["moderate_illness_duration_days"],
        days_in_year=DAYS_IN_YEAR,
        discounted_yll=scalar_data["discounted_yll"],
        population_proportions=agegroup_data["population_proportion"].to_list(),
        hosp_proportions=(
            hosp_proportions[1]
            if hosp_proportions is not None
            else agegroup_data["hosp_proportion"].to_list()
        ),
        outpatient_proportions=(
            outpatient_proportions[1]
            if outpatient_proportions is not None
            else agegroup_data["outpatient_proportion"].to_list()
        ),
        lethality_proportions=agegroup_data["lethality_proportion"].to_list(),
        inpatient_costs=(
            (agegroup_data["inpatient_cost"] * inpatient_costs_factors[1]).to_list()
            if inpatient_costs_factors is not None
            else agegroup_data["inpatient_cost"].to_list()
        ),
        inpatient_pcr_costs=agegroup_data["inpatient_pcr_cost"].to_list(),
        outpatient_ec_costs=(
            (agegroup_data["outpatient_ec_cost"] * outpatient_ec_costs_factors[1]).to_list()
            if outpatient_ec_costs_factors is not None
            else agegroup_data["outpatient_ec_cost"].to_list()
        ),
        outpatient_pc_costs=(
            (agegroup_data["outpatient_pc_cost"] * outpatient_pc_costs_factors[1]).to_list()
            if outpatient_pc_costs_factors is not None
            else agegroup_data["outpatient_pc_cost"].to_list()
        ),
        inpatient_transport_costs=[0.0] * len(age_groups),
        inpatient_caregiver_salary_losses=[0.0] * len(age_groups),
        outpatient_transport_costs=[0.0] * len(age_groups),
        outpatient_caregiver_salary_losses=[0.0] * len(age_groups),
        hosp_reduction_effs=agegroup_data["vaccine_hosp_reduction_eff"].to_list(),
        malrti_reduction_effs=agegroup_data["vaccine_malrti_reduction_eff"].to_list(),
    )

    icer_phs_hi = (nirsevimab_result["cost"] - vaccine_result["cost"]) / (
        vaccine_result["dalys"] - nirsevimab_result["dalys"]
    )

    return {
        "param_name": param_name,
        "icer_soc_lo": icer_soc_lo,
        "icer_soc_hi": icer_soc_hi,
        "icer_phs_lo": icer_phs_lo,
        "icer_phs_hi": icer_phs_hi,
    }


def main():
    univariate_results = []

    univariate_results.append(
        run_univariate("Nirsevimab coverage (50% and 95%)", n_coverage=[0.5, 0.95])
    )
    univariate_results.append(
        run_univariate(
            "Incidence RSV-GB-LRTI-2019 (upper CI – lower CI)",
            hosp_proportions=[[0.0128, 0.0118, 0.0075], [0.0545, 0.0360, 0.0167]],
            outpatient_proportions=[[0.0431, 0.0170, 0.0320], [0.2096, 0.2556, 0.1634]],
        )
    )
    univariate_results.append(
        run_univariate(
            "Inpatient cost (+25% and -25%)",
            inpatient_costs_factors=[0.75, 1.25],
            outpatient_ec_costs_factors=[0.75, 1.25],
        )
    )
    univariate_results.append(
        run_univariate("Outpatient cost (+25% and -25%)", outpatient_pc_costs_factors=[0.75, 1.25])
    )
    univariate_results.append(
        run_univariate(
            "Caregiver wages (+25% and -25%)",
            inpatient_caregiver_salary_losses_factors=[0.75, 1.25],
            outpatient_caregiver_salary_losses_factors=[0.75, 1.25],
        )
    )
    univariate_results.append(
        run_univariate(
            "Nirsevimab effectiveness (upper CI – lower CI)",
            n_hosp_reduction_effs=[[0.72, 0.72, 0.0], [0.79, 0.79, 0.0]],
            n_malrti_reduction_effs=[[0.52, 0.52, 0.0], [0.81, 0.81, 0.0]],
        )
    )

    pd.DataFrame(univariate_results).to_csv(
        "results/univariate/univariate.csv", index=False, encoding="utf-8", lineterminator="\n"
    )


if __name__ == "__main__":
    main()
