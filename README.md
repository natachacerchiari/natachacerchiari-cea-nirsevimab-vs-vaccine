# RSV project

# Cost-Effectiveness Analysis of Nirsevimab vs. Maternal RSV Vaccination in Brazil

This repository contains the Python code for the cost-effectiveness analysis comparing nirsevimab administration to maternal RSV vaccination for preventing RSV disease in Brazilian infants.

## Quick Setup

1. Create the virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## About this project

The analysis is organized into three main components:

    main - The main cost-effectiveness analysis

    univariate - Univariate sensitivity analysis

    psa - Probabilistic sensitivity analysis

    ceac - Cost-effectiveness acceptability curve generation


## Running the scripts

### Main analysis

Run the main cost-effectiveness model:

   ```bash
   python3 main.py
   ```  

### Univariate Sensitivity Analysis

Run the univariate sensitivity analysis:

    ```bash
    python3 univariate.py
    ```

Generate tornado plots for univariate sensitivity analysis results:

    ```bash
    python3 univariate_tornado.py
    ```

### PSA

Execute the probabilistic sensitivity analysis:

   ```bash
   python3 psa.py
   ```
 
### CEAC

Generates cost-effectiveness acceptability curves using incremental costs and DALYs averted from the PSA results.

   ```bash
   python3 ceac.py
   ```

## Output Files

### Univariate Results (saved in results/univariate/ directory)

    univariate.csv - ICER values for each parameter varied in the univariate sensitivity analysis

### PSA results (saved in results/psa/ directory):

    psa_public.csv - Probabilistic sensitivity analysis results from the health system perspective

    psa_societal.csv - Probabilistic sensitivity analysis results from the societal perspective

### CEAC results (saved in results/ceac/ directory):

    ceac_public.csv - ICERs and acceptability probabilities for the health system perspective

    ceac_societal.csv - ICERs and acceptability probabilities for the societal perspective

### Univariate Visualizations (saved in img/univariate/ directory)

    univariate_tornado_phs.png - Tornado diagram for the health system perspective

    univariate_tornado_soc.png - Tornado diagram for the societal perspective

### PSA visualizations (saved in img/psa/ directory):

    psa_scatter_plots.png - Scatter plots comparing cost-effectiveness results for both health system and societal perspectives

### CEAC visualizations (saved in img/ceac/ directory):

    ceac_plots.png - Cost-effectiveness acceptability curves for both health system and societal perspectives

### Analysis Details:

#### Main:

Main Analysis

Calculates incremental cost-effectiveness ratio (ICER) for two perspectives (health system and societal).

Key parameters evaluated:

    Population

    Intervention efficacy: nirsevimab and maternal vaccine

    Cost parameters

    Epidemiological parameters

    Health economics parameters

### Univariate Sensitivity Analysis:

Systematically varies each key parameter individually to assess its impact on the ICER. Parameters evaluated include:

    Nirsevimab coverage (asymmetric and symmetric scenarios)

    Nirsevimab unit price (±25%)

    RSV incidence rates (upper and lower confidence limits)

    Inpatient and outpatient costs (±25%)

    Caregiver daily wage (±25%, societal perspective only)

    Nirsevimab effectiveness (95% confidence intervals)

Results are visualized as tornado diagrams ranking parameters by their influence on the ICER.

#### PSA:

Runs 10,000 iterations using probability distributions specified in data/psa_distributions.py.

Key parameters varied include:

    RSV incidence rates (lognormal distribution)

    Intervention efficacies (beta distribution)

    Cost parameters (lognormal distribution)

    Health utility weights (beta distribution)

All distribution parameters are detailed in Supplementary Table S4 of the associated publication.

#### CEAC:

    Uses PSA results from results/psa/psa_public.csv and results/psa/psa_societal.csv

    Calculates the probability of cost-effectiveness across a range of willingness-to-pay thresholds

    Generates curves showing the proportion of iterations considered cost-effective at each threshold value

