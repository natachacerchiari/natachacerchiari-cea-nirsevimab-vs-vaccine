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

    psa - Probabilistic sensitivity analysis

    ceac - Cost-effectiveness acceptability curve generation


## Running the scripts

### Main analysis

Run the main cost-effectiveness model:

   ```bash
   python3 main.py
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

### PSA results (saved in results/psa/ directory):

    psa_public.csv - Probabilistic sensitivity analysis results from the health system perspective

    psa_societal.csv - Probabilistic sensitivity analysis results from the societal perspective

### CEAC results (saved in results/ceac/ directory):

    ceac_public.csv - ICERs and acceptability probabilities for the health system perspective

    ceac_societal.csv - ICERs and acceptability probabilities for the societal perspective

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

