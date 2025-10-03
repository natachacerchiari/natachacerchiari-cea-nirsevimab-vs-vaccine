import pandas as pd
from util.core import (
    calculate_discounted_yll,
    calculate_dose_cost,
    calculate_inpatient_transport_cost,
    calculate_outpatient_transport_cost,
    calculate_salary_loss,
)

__all__ = ["enrich_scalar_data", "enrich_agegroup_data"]


def enrich_scalar_data(scalar_data: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich the scalar data by adding:
      - discounted_yll
      - nirsevimab_dose_cost
      - vaccine_dose_cost
    """
    required_yll_cols = {
        'discount_rate',
        'life_expectancy_floor',
        'life_expectancy_last_year_remainder'
    }
    if not required_yll_cols.issubset(scalar_data.columns):
        raise ValueError(f"Input DataFrame must contain {required_yll_cols} columns.")
    scalar_data['discounted_yll'] = scalar_data.apply(
        lambda row: calculate_discounted_yll(
            discount_rate=row['discount_rate'],
            years=row['life_expectancy_floor'],
            final_year_factor=row['life_expectancy_last_year_remainder']
        ),
        axis=1
    )

    required_cost_cols = {
        'nirsevimab_unit_cost',
        'nirsevimab_wastage_rate',
        'nirsevimab_administration_cost',
        'vaccine_unit_cost',
        'vaccine_wastage_rate',
        'vaccine_administration_cost'
    }
    if not (required_cost_cols).issubset(scalar_data.columns):
        raise ValueError(f"Input DataFrame must contain {required_cost_cols} columns.")
    scalar_data['nirsevimab_dose_cost'] = scalar_data.apply(
        lambda r: calculate_dose_cost(
            r['nirsevimab_unit_cost'],
            r['nirsevimab_wastage_rate'],
            r['nirsevimab_administration_cost']
        ),
        axis=1
    )
    scalar_data['vaccine_dose_cost'] = scalar_data.apply(
        lambda r: calculate_dose_cost(
            r['vaccine_unit_cost'],
            r['vaccine_wastage_rate'],
            r['vaccine_administration_cost']
        ),
        axis=1
    )
    return scalar_data


def enrich_agegroup_data(agegroup_data: pd.DataFrame, scalar_data: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich age group data by adding:
        - inpatient_transport_cost
        - outpatient_transport_cost
        - inpatient_caregiver_salary_loss
        - outpatient_caregiver_salary_loss
    """
    if scalar_data.shape[0] != 1:
        raise ValueError("scalar_data must contain exactly one row.")
    scalar_row = scalar_data.iloc[0]

    required_scalar_cols = {
        'moderate_illness_duration_days',
        'severe_illness_duration_days'
    }
    if not required_scalar_cols.issubset(scalar_data.columns):
        raise ValueError(f"Input DataFrame must contain {required_scalar_cols} columns.")

    required_agegroup_cols = {
        'caregiver_visit_days',
        'consultations',
        'transport_cost_per_trip',
        'affected_caregivers_proportion',
        'caregiver_daily_salary'
    }
    if not required_agegroup_cols.issubset(agegroup_data.columns):
        raise ValueError(f"Input DataFrame must contain {required_agegroup_cols} columns.")

    agegroup_data["inpatient_transport_cost"] = agegroup_data.apply(
        lambda r: calculate_inpatient_transport_cost(
            caregiver_visit_days=r["caregiver_visit_days"],
            consultations=r["consultations"],
            transport_cost_per_trip=r["transport_cost_per_trip"],
        ),
        axis=1,
    )
    agegroup_data["outpatient_transport_cost"] = agegroup_data.apply(
        lambda r: calculate_outpatient_transport_cost(
            consultations=r["consultations"],
            transport_cost_per_trip=r["transport_cost_per_trip"],
        ),
        axis=1,
    )

    moderate_duration = scalar_row["moderate_illness_duration_days"]
    agegroup_data["outpatient_caregiver_salary_loss"] = agegroup_data.apply(
        lambda r: calculate_salary_loss(
            illness_duration_days=moderate_duration,
            affected_caregivers_proportion=r["affected_caregivers_proportion"],
            caregiver_daily_salary=r["caregiver_daily_salary"],
        ),
        axis=1,
    )

    severe_duration = scalar_row["severe_illness_duration_days"]
    agegroup_data["inpatient_caregiver_salary_loss"] = agegroup_data.apply(
        lambda r: calculate_salary_loss(
            illness_duration_days=severe_duration,
            affected_caregivers_proportion=r["affected_caregivers_proportion"],
            caregiver_daily_salary=r["caregiver_daily_salary"],
        ),
        axis=1,
    )
    return agegroup_data
