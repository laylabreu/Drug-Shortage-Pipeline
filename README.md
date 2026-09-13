# BioamineMal

**Linking patient biomarkers, mosquito behavior, and temperature to malaria transmission risk.**

A computational pipeline that tests whether patient blood chemistry — specifically elevated histamine and depleted serotonin, seen in severe malaria — changes mosquito behavior in ways that measurably alter outbreak dynamics. Built as part of the Fralin Summer Undergraduate Research Fellowship, Virginia Tech.

---

## Overview

Standard malaria transmission models treat mosquito biting behavior as a fixed parameter. They don't account for the possibility that a patient's own blood chemistry — altered during severe infection — could change how the mosquito that just bit them behaves next. This project builds and tests that connection end-to-end: from raw experimental and clinical data, through machine learning models of mosquito activity, into a full epidemiological transmission simulation.

**Research question:** Can integrating patient biomarkers for histamine and serotonin, mosquito behavior, and temperature into models provide important insights that simpler models miss?

**Hypothesis:** Elevated histamine and reduced serotonin during severe malaria (referred to here as **MABAC** — Malaria-Associated Biogenic Amine Combination) increase mosquito activity in ways that compound with rising temperature, producing a disproportionate transmission risk not captured by standard models. The healthy counterpart (low histamine, high serotonin) is referred to as **HABAC**.

---

## Headline Results

| Scenario | Peak Infection Change | Timing Shift |
|---|---|---|
| MABAC only | +10.2% | 53 days earlier |
| MABAC + 31°C (simple model) | +52.9% | 236 days earlier |
| MABAC + 31°C (age-structured, mortality-adjusted) | +22.9% | 142 days earlier |

*All comparisons against a baseline scenario using healthy (HABAC) biomarker levels.*

The core finding: biomarker and temperature effects **compound rather than add** — the combined effect substantially exceeds what either factor produces alone. This holds even after accounting for realistic mosquito mortality, where only an estimated 34% of infected mosquitoes survive long enough to become infectious.

---

## Project Structure

The project is organized into four sequential modules:

### Module 1 — Data Pipeline
A fully automated, reproducible pipeline (Python, Snakemake) integrating four independent data sources:

| Source | Description |
|---|---|
| Simulated patient biomarkers | 900 simulated patients (healthy/mild/severe), histamine and serotonin distributions grounded in Enwonwu et al. (2000) and Badcock et al. (1987) |
| Mosquito behavioral data | 47,520 real *Anopheles stephensi* activity measurements, Fralin Life Sciences Institute (unpublished) |
| CDC malaria surveillance data | 51 years (1972–2022) of U.S. case data |
| Climate data | 4,748 days (2010–2022) of real historical temperature data for Abuja, Nigeria, via the Open-Meteo API |

Rebuildable end-to-end with a single command via Snakemake, with built-in validation checks (row counts, category consistency, cross-field totals) at every ingestion step.

### Module 2 — Exploratory Analysis
Statistical analysis of mosquito behavioral data across biomarker level, temperature, infection status, and infection day. Key findings:
- MABAC uniquely shifts peak mosquito activity to 31°C (vs. 28°C for HABAC and controls)
- Biomarker level has a larger effect on activity than infection status alone
- Activity peaks at day 10 post-infection across all treatment groups

### Module 3 — Machine Learning
Random forest models predicting mosquito activity from biomarker treatment level combined with either infection day or temperature.
- Individual-level prediction performed near chance (ROC AUC = 0.573) — a genuine finding about the limits of individual-level behavioral prediction, not a modeling failure
- Group-level aggregated prediction performed strongly (R² = 0.837 for infection day, R² = 0.918 for temperature)
- Feature importance analysis quantified the relative contribution of biomarker level vs. environmental/temporal factors

### Module 4 — Transmission Model
An extended SEIR (Susceptible-Exposed-Infected-Recovered) model using the Ross-Macdonald force-of-infection framework, parameterized with published values from Chitnis et al. (2008) and Dudley et al. (2015).
- Baseline model validated via R0 = 7.254, consistent with sustained transmission dynamics in comparable published models
- Extended with a 22% transmission-probability increase derived from histamine-exposure data (Rodriguez et al., 2021) and a machine-learning-derived biting-rate adjustment
- Further refined with an age-structured mortality model, incorporating *Anopheles stephensi* mortality data (Dawes et al., 2009) to account for the proportion of infected mosquitoes that die before reaching the infectious stage
- Waning immunity (Dudley et al., 2015) incorporated to produce a realistic sustained endemic equilibrium rather than a single outbreak wave

---

## Repository Structure

```
BioamineMal/
├── data/
│   ├── raw/                  # Original experimental and simulated source files
│   ├── external/             # Third-party downloaded data (CDC)
│   └── processed/            # Cleaned, validated, analysis-ready datasets
├── src/
│   └── pipeline/             # Ingestion, validation, and simulation scripts
│       ├── ingest_epidemiology.py
│       ├── ingest_biomarker.py
│       ├── ingest_behavioral.py
│       ├── ingest_climate.py
│       ├── simulate_patient_biomarkers.py
│       └── database.py
├── notebooks/
│   ├── exploratory_analysis.ipynb
│   ├── ml_models.ipynb
│   └── transmission_model.ipynb
├── results/
│   ├── figures/               # Saved visualizations
│   └── tables/                # Saved summary statistics
├── app.py                     # Interactive Streamlit decision-support tool
├── Snakefile                  # Pipeline orchestration
└── README.md
```

---

## Tech Stack

- **Python** — pandas, NumPy, scikit-learn, Matplotlib, joblib
- **Snakemake** — pipeline orchestration and reproducibility
- **Streamlit** — interactive web application
- **Git/GitHub** — version control

---

## Getting Started

**Rebuild the full data pipeline from scratch:**
```bash
snakemake --cores 1
```

**Run the interactive transmission risk simulator:**
```bash
streamlit run app.py
```

**Explore the analysis notebooks:**
```
notebooks/exploratory_analysis.ipynb   # Module 2
notebooks/ml_models.ipynb              # Module 3
notebooks/transmission_model.ipynb     # Module 4
```

---

## Limitations

- Aggregated machine learning models were trained on a limited number of unique experimental conditions (15–18), meaning a formal train/test split was not feasible at this scale.
- Stage-specific mosquito mortality parameters were derived from *Anopheles stephensi* infected with *Plasmodium berghei* (Dawes et al., 2009), the closest available proxy, since no equivalent stage-specific mortality data exists for the *Plasmodium falciparum*–histamine–serotonin system studied here.
- Patient biomarker data is simulated from published clinical distributions rather than drawn from real, individual patient measurements.

## Future Directions

- Incorporate real seasonal temperature variation using the project's existing 13-year Abuja climate dataset, allowing biting rate to fluctuate dynamically over a simulated year
- Build a fully age-structured mosquito population model tracking sequential infection stages explicitly over time
- Integrate patient, climate, and case data from a single real-world location to test the full pipeline in one region

---

## References

- Rodriguez, N. et al. (2021). Histamine ingestion by *Anopheles stephensi* alters important vector transmission behaviors and infection success with diverse *Plasmodium* species. *Biomolecules*.
- Briggs, K. et al. (2022). Serotonin and mosquito behavior. *Frontiers in Physiology*.
- Coles, V. et al. (2023). Combined histamine-serotonin behavioral and transmission modeling.
- Ochwedo, K. et al. (2025). Temperature-biomarker interaction effects on mosquito behavior.
- Enwonwu, C. et al. (2000). Increased plasma levels of histidine and histamine in falciparum malaria: relevance to severity of infection. *Journal of Neural Transmission*.
- Badcock, N. et al. (1987). Blood serotonin levels in adults. *Annals of Clinical Biochemistry*.
- Chitnis, N., Hyman, J., Cushing, J. (2008). Determining important parameters in the spread of malaria through sensitivity analysis of a mathematical model. *Bulletin of Mathematical Biology*.
- Dudley, H. et al. (2015). Multi-year optimization of malaria intervention: a mathematical model.
- Dawes, E. et al. (2009). Age- and density-dependent survival of *Anopheles stephensi* infected with *Plasmodium berghei*. *Malaria Journal*.
- World Health Organization (2025). World Malaria Report.

---

## Author

**Layla Abreu**
B.S. Computational Modeling & Data Analytics, Minors in Computer Science and Mathematics, Virginia Tech
Fralin Summer Undergraduate Research Fellowship, Fralin Life Sciences Institute
Mentor: Dr. Michael Robert, Department of Mathematics, Virginia Tech
