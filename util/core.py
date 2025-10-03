"""Core reusable functions for the VSR project."""

__all__ = ["calculate_discounted_yll", "calculate_dose_cost",
           "calculate_inpatient_transport_cost", "calculate_outpatient_transport_cost",
           "calculate_salary_loss", "run_scenario"]

from typing import Sequence, Dict


def _compute_cases_with_eff(population: float, proportion: float, reduction_eff: float) -> float:
    return population * proportion * (1 - reduction_eff)


def _compute_death_cases(cases: float, lethality: float) -> float:
    return cases * lethality


def _compute_cure_cases(cases: float, deaths: float) -> float:
    return cases - deaths


def _calculate_subgroup_cost(
    population: float,
    hosp_proportion: float,
    outpatient_proportion: float,
    hosp_reduction_eff: float,
    malrti_reduction_eff: float,
    inpatient_cost: float,
    inpatient_pcr_cost: float,
    inpatient_transport_cost: float,
    inpatient_salary_loss: float,
    outpatient_ec_cost: float,  # Emergency care
    outpatient_pc_cost: float,  # Primary care
    outpatient_transport_cost: float,
    outpatient_salary_loss: float,
) -> float:
    """
    Calculate total economic cost for a subgroup
    as the sum of inpatient and outpatient costs.
    """

    hosp_cases = _compute_cases_with_eff(
        population, hosp_proportion, hosp_reduction_eff)
    outpatient_cases = _compute_cases_with_eff(
        population, outpatient_proportion, malrti_reduction_eff)

    inpatient_base = (
        inpatient_cost
        + inpatient_pcr_cost
        + inpatient_transport_cost
        + inpatient_salary_loss
        + outpatient_ec_cost  # At least one emergency care visit
    )
    outpatient_base = (
        outpatient_pc_cost
        + outpatient_transport_cost
        + outpatient_salary_loss
    )

    total_cost = hosp_cases * inpatient_base + outpatient_cases * outpatient_base
    return total_cost


def _calculate_subgroup_dalys(
    population: float,
    hosp_proportion: float,
    outpatient_proportion: float,
    hosp_reduction_eff: float,
    malrti_reduction_eff: float,
    severe_case_dw: float,  # disability weight
    moderate_case_dw: float,  # disability weight
    severe_illness_duration_days: float,
    moderate_illness_duration_days: float,
    lethality: float,
    days_in_year: float,
    discounted_yll: float,
) -> float:
    """
    Calculate total DALYs (morbidity + mortality) for a subgroup.

    DALY components:
      Severe hospitalized (cured) morbidity
      Moderate outpatient morbidity
      Severe hospitalized (fatal) morbidity
      Years of Life Lost (discounted)
    """
    if days_in_year <= 0:
        raise ValueError("days_in_year must be > 0.")

    hosp_cases = _compute_cases_with_eff(
        population, hosp_proportion, hosp_reduction_eff)
    outpatient_cases = _compute_cases_with_eff(
        population, outpatient_proportion, malrti_reduction_eff)
    hosp_death_cases = _compute_death_cases(hosp_cases, lethality)
    hosp_cure_cases = _compute_cure_cases(hosp_cases, hosp_death_cases)

    # Condition mean duration (in years)
    hosp_duration_years = severe_illness_duration_days / days_in_year
    outpatient_duration_years = moderate_illness_duration_days / days_in_year

    # Hospitalized cases (cured and fatal)
    hosp_cure_daly = hosp_cure_cases * severe_case_dw * hosp_duration_years
    hosp_death_daly = hosp_death_cases * severe_case_dw * hosp_duration_years
    yll_daly = hosp_death_cases * discounted_yll

    hosp_daly = hosp_cure_daly + hosp_death_daly + yll_daly

    # Outpatient cases (all cured)
    outpatient_daly = outpatient_cases * moderate_case_dw * outpatient_duration_years

    return hosp_daly + outpatient_daly


def calculate_discounted_yll(discount_rate: float, years: int, final_year_factor: float) -> float:
    """
    Compute the present value (discounted) of Years of Life Lost (YLL).

    Parameters:
        discount_rate (float): Annual discount rate (must be > -1).
        years (int): Number of complete years (must be >= 0).
        final_year_factor (float): Fractional part of the terminal (partial) year (typically in [0, 1]).

    Returns:
        float: Discounted YLL value.
    """
    # Base discount factor
    base = 1.0 / (1.0 + discount_rate)

    # Sum of full-year discounted factors
    if years > 0:
        sum_discounts = sum(base ** t for t in range(int(years)))
    else:
        sum_discounts = 0.0

    # Discount factor for the (possibly partial) terminal year
    final_discount = base ** years
    return sum_discounts + final_discount * final_year_factor


def calculate_dose_cost(unit_cost: float, wastage_pct: float, administration_cost: float) -> float:
    """
    Calculate the per-dose cost including wastage and admnistration costs.
    """
    dose_cost = unit_cost * (1 + wastage_pct) + administration_cost
    return dose_cost


def calculate_inpatient_transport_cost(caregiver_visit_days: float, consultations: float, transport_cost_per_trip: float) -> float:
    """
    Calculate inpatient transport cost per patient considering round trips.
    """
    visits = caregiver_visit_days + consultations
    inpatient_transport_cost = visits * 2 * \
        transport_cost_per_trip  # times 2 for round trip
    return inpatient_transport_cost


def calculate_outpatient_transport_cost(consultations: float, transport_cost_per_trip: float) -> float:
    """
    Calculate outpatient transport cost per patient considering round trips.
    """
    outpatient_transport_cost = consultations * 2 * \
        transport_cost_per_trip  # times 2 for round trip
    return outpatient_transport_cost


def calculate_salary_loss(illness_duration_days: float, affected_caregivers_proportion: float, caregiver_daily_salary: float) -> float:
    """
    Calculate average caregiver salary loss per patient.
    """
    salary_loss = illness_duration_days * \
        affected_caregivers_proportion * caregiver_daily_salary
    return salary_loss


def run_scenario(
    cohort: float,
    coverage: float,
    intervention_dose_cost: float,
    severe_case_dw: float,
    moderate_case_dw: float,
    severe_illness_duration_days: float,
    moderate_illness_duration_days: float,
    days_in_year: float,
    discounted_yll: float,
    # per-subgroup epidemiologic proportions lists
    population_proportions: Sequence[float],  # (must sum ~1)
    hosp_proportions: Sequence[float],
    outpatient_proportions: Sequence[float],
    lethality_proportions: Sequence[float],
    # per-subgroup cost lists
    inpatient_costs: Sequence[float],
    inpatient_pcr_costs: Sequence[float],
    outpatient_ec_costs: Sequence[float],
    outpatient_pc_costs: Sequence[float],
    inpatient_transport_costs: Sequence[float],
    inpatient_caregiver_salary_losses: Sequence[float],
    outpatient_transport_costs: Sequence[float],
    outpatient_caregiver_salary_losses: Sequence[float],
    # per-subgroup effectiveness lists
    hosp_reduction_effs: Sequence[float],
    malrti_reduction_effs: Sequence[float],
) -> Dict[str, float]:
    """
    Run an intervention scenario across multiple subgroups.

    Returns:
        Dict[str, float]: {"cost": total_cost, "dalys": total_dalys}
    """
    seqs = [
        population_proportions, hosp_proportions, outpatient_proportions, lethality_proportions,
        inpatient_costs, inpatient_pcr_costs, outpatient_ec_costs, outpatient_pc_costs,
        inpatient_transport_costs, inpatient_caregiver_salary_losses,
        outpatient_transport_costs, outpatient_caregiver_salary_losses,
        hosp_reduction_effs, malrti_reduction_effs,
    ]
    lengths = [len(s) for s in seqs]
    if len(set(lengths)) != 1:
        raise ValueError(
            f"All subgroup sequences must have identical length. Got lengths: {lengths}")
    n = lengths[0]
    if n == 0:
        return {"cost": cohort * coverage * intervention_dose_cost, "dalys": 0.0}

    total_prop = sum(population_proportions)
    if not (0.999 <= total_prop <= 1.001):
        # Allow a small tolerance but enforce near-1 total
        raise ValueError(
            f"Subgroup proportions must sum to 1 (±0.001). Got {total_prop}.")

    total_disease_cost = 0.0
    total_dalys = 0.0

    for i in range(n):
        group_pop = cohort * population_proportions[i]
        treated_pop = group_pop * coverage
        untreated_pop = group_pop * (1 - coverage)

        # Costs
        cost_treated = _calculate_subgroup_cost(
            treated_pop,
            hosp_proportions[i],
            outpatient_proportions[i],
            hosp_reduction_effs[i],
            malrti_reduction_effs[i],
            inpatient_costs[i],
            inpatient_pcr_costs[i],
            inpatient_transport_costs[i],
            inpatient_caregiver_salary_losses[i],
            outpatient_ec_costs[i],
            outpatient_pc_costs[i],
            outpatient_transport_costs[i],
            outpatient_caregiver_salary_losses[i],
        )
        cost_untreated = _calculate_subgroup_cost(
            untreated_pop,
            hosp_proportions[i],
            outpatient_proportions[i],
            0.0,
            0.0,
            inpatient_costs[i],
            inpatient_pcr_costs[i],
            inpatient_transport_costs[i],
            inpatient_caregiver_salary_losses[i],
            outpatient_ec_costs[i],
            outpatient_pc_costs[i],
            outpatient_transport_costs[i],
            outpatient_caregiver_salary_losses[i],
        )
        total_disease_cost += cost_treated + cost_untreated

        # DALYs
        dalys_treated = _calculate_subgroup_dalys(
            treated_pop,
            hosp_proportions[i],
            outpatient_proportions[i],
            hosp_reduction_effs[i],
            malrti_reduction_effs[i],
            severe_case_dw,
            moderate_case_dw,
            severe_illness_duration_days,
            moderate_illness_duration_days,
            lethality_proportions[i],
            days_in_year,
            discounted_yll,
        )

        dalys_untreated = _calculate_subgroup_dalys(
            untreated_pop,
            hosp_proportions[i],
            outpatient_proportions[i],
            0.0,
            0.0,
            severe_case_dw,
            moderate_case_dw,
            severe_illness_duration_days,
            moderate_illness_duration_days,
            lethality_proportions[i],
            days_in_year,
            discounted_yll,
        )
        total_dalys += dalys_treated + dalys_untreated

    total_intervention_cost = cohort * coverage * intervention_dose_cost
    return {
        "cost": total_disease_cost + total_intervention_cost,
        "dalys": total_dalys,
    }
