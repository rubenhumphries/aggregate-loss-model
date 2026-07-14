# Actuarial Risk Model

Monte Carlo simulation of aggregate insurance losses using a compound Poisson–Lognormal frequency-severity model. The project demonstrates how stochastic simulation can be used to estimate portfolio losses and calculate common actuarial risk measures.

---

## Overview

This project models annual aggregate insurance losses by combining:

- **Claim frequency** using a Poisson distribution
- **Claim severity** using a Lognormal distribution
- **Monte Carlo simulation** to generate annual loss distributions

The model also applies a simple **per-claim excess-of-loss reinsurance treaty** and evaluates its impact on aggregate losses.

---

## Mathematical Model

Annual aggregate loss is modelled as

S = X₁ + X₂ + ... + Xₙ

where

N follows a Poisson distribution with parameter λ.

Each claim amount X follows a Lognormal distribution with parameters μ and σ.

A per-claim excess-of-loss reinsurance layer is applied with:

- Attachment point: **£10,000**
- Limit: **£50,000**

---

## Risk Measures

For each simulated portfolio the model calculates:

- Mean annual loss
- Standard deviation
- 95% Value at Risk (VaR)
- 99% Value at Risk (VaR)
- 99% Expected Shortfall (ES)

Sensitivity analysis is performed for different claim frequencies:

- λ = 5
- λ = 10
- λ = 15
- λ = 20

--- 

## Sample Outputs

### Aggregate Loss Distribution

![Aggregate Loss Distribution](results/plots/loss_distribution.png)

### Claim Severity Distribution

![Claim Severity Distribution](results/plots/claim_severity.png)

### Mean Annual Loss vs Claim Frequency

![Mean Loss](results/plots/mean_loss_sensitivity.png)

### VaR 99% vs Claim Frequency

![VaR 99](results/plots/var99_sensitivity.png)

---

## Project Structure

```
actuarial-risk-model/

├── aggregate_loss_model.py
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
└── results/
    ├── plots/
    │   ├── claim_severity.png
    │   ├── frequency_sensitivity_distribution.png
    │   ├── loss_distribution.png
    │   ├── mean_loss_sensitivity.png
    │   └── var99_sensitivity.png
    │
    └── tables/
        └── aggregate_claim_results.csv
```

---

## Example Output

The simulation produces:

- Aggregate annual loss distributions
- Claim severity distribution
- Sensitivity of mean annual loss to claim frequency
- Sensitivity of 99% VaR to claim frequency
- Summary table containing simulated risk measures

---

## Installation

Clone the repository:

```bash
git clone https://github.com/rubenhumphries/aggregate-loss-model/tree/main/actuarial_risk_model
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the model:

```bash
python aggregate_loss_model.py
```

---

## Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib

---

## Future Improvements

Potential extensions include:

- Alternative severity distributions (Gamma, Pareto, Weibull)
- Frequency calibration from real claims data
- Gross versus net reinsurance comparison
- Catastrophe loss modelling
- Capital modelling under Solvency II
- Parameter estimation using maximum likelihood

---

## Author

Ruben

Mathematics graduate with an interest in actuarial science, stochastic modelling and quantitative risk analysis.
