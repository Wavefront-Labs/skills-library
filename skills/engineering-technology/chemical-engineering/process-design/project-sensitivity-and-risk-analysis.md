---
id: engineering-technology.chemical-engineering.process-design.project-sensitivity-and-risk-analysis
name: project-sensitivity-and-risk-analysis
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-profitability-analysis, project-sensitivity-and-risk-analysis, sensitivity-analysis, tornado-chart, monte-carlo, risk-analysis, break-even, scenario-analysis, project-risk, npv-sensitivity]
level: practitioner
status: draft
description: "Run sensitivity (tornado) and Monte Carlo risk analysis on project NPV: choose variables and ranges, interpret results, and report break-even values."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics, Douglas Conceptual Design of Chemical Processes, NCEES FE and PE Chemical exam specifications"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sensitivity and risk analysis of project economics

**Goal:** show which assumptions control the decision and how likely a loss is.

## One-at-a-time sensitivity
1. Choose variables: product price, feed price, energy price, capital cost, production rate, conversion/yield, discount rate, schedule delay.
2. Choose realistic ranges (for example capital -20/+40% at class 4, price from historical volatility).
3. Vary each alone, recompute NPV, plot a **tornado chart** sorted by swing.
4. Report **break-even** values: the price or capital at which NPV = 0.

## Scenario analysis
Define 3 or 4 coherent scenarios (low-price, base, high-price, delayed ramp-up) with correlated changes in several variables.

## Monte Carlo
1. Assign distributions (triangular with min/likely/max is common) to the main uncertain inputs.
2. Define correlations (product price and feed price are often correlated).
3. Run thousands of trials; report P10, P50, P90 NPV and the probability NPV < 0.
4. Rank contributors to variance.

## Gotchas
- Independent sampling of correlated variables understates risk.
- Ranges set by the project team tend to be too narrow.
- A tornado chart shows linear effects only; combine with scenarios for interaction.

## Verify
- [ ] Base case NPV reproduced at the centre of all plots.
- [ ] The two or three dominant variables flagged to management with mitigations.
