from util.core import run_scenario
from util.constants import DAYS_IN_YEAR
from util.data_loader import load_age_groups, load_scalar_data, load_agegroup_data
from util.data_enricher import enrich_scalar_data, enrich_agegroup_data


def main():
    age_groups = load_age_groups()
    scalar_data = enrich_scalar_data(load_scalar_data())
    agegroup_data = enrich_agegroup_data(load_agegroup_data(), scalar_data)
    scalar_data = scalar_data.iloc[0]

    # Perspective: societal (direct + indirect costs)

    print("=== Societal perspective ===")

    nirsevimab_result = run_scenario(
        cohort=scalar_data["cohort"],
        coverage=scalar_data["nirsevimab_coverage"],
        intervention_dose_cost=scalar_data["nirsevimab_dose_cost"],
        severe_case_dw=scalar_data["severe_case_dw"],
        moderate_case_dw=scalar_data["moderate_case_dw"],
        severe_illness_duration_days=scalar_data["severe_illness_duration_days"],
        moderate_illness_duration_days=scalar_data["moderate_illness_duration_days"],
        days_in_year=DAYS_IN_YEAR,
        discounted_yll=scalar_data["discounted_yll"],
        population_proportions=agegroup_data["population_proportion"].to_list(),
        hosp_proportions=agegroup_data["hosp_proportion"].to_list(),
        outpatient_proportions=agegroup_data["outpatient_proportion"].to_list(),
        lethality_proportions=agegroup_data["lethality_proportion"].to_list(),
        inpatient_costs=agegroup_data["inpatient_cost"].to_list(),
        inpatient_pcr_costs=agegroup_data["inpatient_pcr_cost"].to_list(),
        outpatient_ec_costs=agegroup_data["outpatient_ec_cost"].to_list(),
        outpatient_pc_costs=agegroup_data["outpatient_pc_cost"].to_list(),
        inpatient_transport_costs=agegroup_data["inpatient_transport_cost"].to_list(),
        inpatient_caregiver_salary_losses=agegroup_data["inpatient_caregiver_salary_loss"].to_list(),
        outpatient_transport_costs=agegroup_data["outpatient_transport_cost"].to_list(),
        outpatient_caregiver_salary_losses=agegroup_data["outpatient_caregiver_salary_loss"].to_list(),
        hosp_reduction_effs=agegroup_data["nirsevimab_hosp_reduction_eff"].to_list(),
        malrti_reduction_effs=agegroup_data["nirsevimab_malrti_reduction_eff"].to_list(),
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
        hosp_proportions=agegroup_data["hosp_proportion"].to_list(),
        outpatient_proportions=agegroup_data["outpatient_proportion"].to_list(),
        lethality_proportions=agegroup_data["lethality_proportion"].to_list(),
        inpatient_costs=agegroup_data["inpatient_cost"].to_list(),
        inpatient_pcr_costs=agegroup_data["inpatient_pcr_cost"].to_list(),
        outpatient_ec_costs=agegroup_data["outpatient_ec_cost"].to_list(),
        outpatient_pc_costs=agegroup_data["outpatient_pc_cost"].to_list(),
        inpatient_transport_costs=agegroup_data["inpatient_transport_cost"].to_list(),
        inpatient_caregiver_salary_losses=agegroup_data["inpatient_caregiver_salary_loss"].to_list(),
        outpatient_transport_costs=agegroup_data["outpatient_transport_cost"].to_list(),
        outpatient_caregiver_salary_losses=agegroup_data["outpatient_caregiver_salary_loss"].to_list(),
        hosp_reduction_effs=agegroup_data["vaccine_hosp_reduction_eff"].to_list(),
        malrti_reduction_effs=agegroup_data["vaccine_malrti_reduction_eff"].to_list(),
    )

    print("Vaccine scenario:", vaccine_result)
    print("Nirsevimab scenario:", nirsevimab_result)

    icer = (nirsevimab_result["cost"] - vaccine_result["cost"]) / (
        vaccine_result["dalys"] - nirsevimab_result["dalys"]
    )

    print("ICER: ", icer)

    # Perspective: public health system (direct costs only)

    print("=== Public health system perspective ===")

    nirsevimab_result = run_scenario(
        cohort=scalar_data["cohort"],
        coverage=scalar_data["nirsevimab_coverage"],
        intervention_dose_cost=scalar_data["nirsevimab_dose_cost"],
        severe_case_dw=scalar_data["severe_case_dw"],
        moderate_case_dw=scalar_data["moderate_case_dw"],
        severe_illness_duration_days=scalar_data["severe_illness_duration_days"],
        moderate_illness_duration_days=scalar_data["moderate_illness_duration_days"],
        days_in_year=DAYS_IN_YEAR,
        discounted_yll=scalar_data["discounted_yll"],
        population_proportions=agegroup_data["population_proportion"].to_list(),
        hosp_proportions=agegroup_data["hosp_proportion"].to_list(),
        outpatient_proportions=agegroup_data["outpatient_proportion"].to_list(),
        lethality_proportions=agegroup_data["lethality_proportion"].to_list(),
        inpatient_costs=agegroup_data["inpatient_cost"].to_list(),
        inpatient_pcr_costs=agegroup_data["inpatient_pcr_cost"].to_list(),
        outpatient_ec_costs=agegroup_data["outpatient_ec_cost"].to_list(),
        outpatient_pc_costs=agegroup_data["outpatient_pc_cost"].to_list(),
        inpatient_transport_costs=agegroup_data["inpatient_transport_cost"].to_list(),
        inpatient_caregiver_salary_losses=[0.0] * len(age_groups),
        outpatient_transport_costs=agegroup_data["outpatient_transport_cost"].to_list(),
        outpatient_caregiver_salary_losses=[0.0] * len(age_groups),
        hosp_reduction_effs=agegroup_data["nirsevimab_hosp_reduction_eff"].to_list(),
        malrti_reduction_effs=agegroup_data["nirsevimab_malrti_reduction_eff"].to_list(),
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
        hosp_proportions=agegroup_data["hosp_proportion"].to_list(),
        outpatient_proportions=agegroup_data["outpatient_proportion"].to_list(),
        lethality_proportions=agegroup_data["lethality_proportion"].to_list(),
        inpatient_costs=agegroup_data["inpatient_cost"].to_list(),
        inpatient_pcr_costs=agegroup_data["inpatient_pcr_cost"].to_list(),
        outpatient_ec_costs=agegroup_data["outpatient_ec_cost"].to_list(),
        outpatient_pc_costs=agegroup_data["outpatient_pc_cost"].to_list(),
        inpatient_transport_costs=agegroup_data["inpatient_transport_cost"].to_list(),
        inpatient_caregiver_salary_losses=[0.0] * len(age_groups),
        outpatient_transport_costs=agegroup_data["outpatient_transport_cost"].to_list(),
        outpatient_caregiver_salary_losses=[0.0] * len(age_groups),
        hosp_reduction_effs=agegroup_data["vaccine_hosp_reduction_eff"].to_list(),
        malrti_reduction_effs=agegroup_data["vaccine_malrti_reduction_eff"].to_list(),
    )

    print("Vaccine scenario:", vaccine_result)
    print("Nirsevimab scenario:", nirsevimab_result)

    icer = (nirsevimab_result["cost"] - vaccine_result["cost"]) / (
        vaccine_result["dalys"] - nirsevimab_result["dalys"]
    )

    print("ICER: ", icer)


if __name__ == "__main__":
    main()
