---
id: computing-software.ai-ml-engineering.feature-engineering.deletion-vs-imputation-tradeoffs
name: deletion-vs-imputation-tradeoffs
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, listwise-deletion, complete-case-analysis, missing-data, imputation, mcar, column-dropping]
level: practitioner
status: verified
description: "Decide between dropping rows, dropping columns and imputing missing values: bias under MCAR/MAR/MNAR, sample-size loss, serving-time consequences and how to test the choice."
sources:
  - https://stefvanbuuren.name/fimd/
  - https://scikit-learn.org/stable/modules/impute.html
  - https://pandas.pydata.org/docs/user_guide/missing_data.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Deletion vs imputation trade-offs

## Options
| Option | What | Risk |
|---|---|---|
| Listwise (complete-case) deletion | drop rows with any missing value | bias unless MCAR; large sample loss with many columns |
| Pairwise deletion | use available pairs per statistic (correlations) | inconsistent estimates; not usable for model training |
| Drop column | remove features with too many missing | lose signal (missingness itself may be predictive) |
| Impute | fill (mean/median/model-based/MICE) + indicator | distorted variance if single imputation used for inference |
| Native handling | models that accept NaN (HistGB, XGBoost, LightGBM) | model-specific |

## Bias depends on the mechanism
- **MCAR** (missing completely at random): deletion is unbiased, just less data.
- **MAR** (missing depends on observed variables): deletion biases results; imputation conditional on observed variables (iterative/MICE) can correct.
- **MNAR** (depends on the unobserved value itself, e.g. high earners skip income): neither fixes it; missingness indicators and domain modelling help prediction, but inference stays biased.
Check: compare distributions of other variables between rows with and without missing values; a classifier predicting missingness from other features with AUC >> 0.5 rules out MCAR.

## Sample loss arithmetic
With 20 columns each 5% missing independently, complete cases = 0.95^20 = 35.8% of rows (computed). Listwise deletion throws away two thirds of the data.

## Predictive modelling rules of thumb
- **Never drop rows at training time that you must score at prediction time.** If production rows have missing values, the model must handle them; drop-row training makes the model untested on exactly those cases.
- Drop rows only when the **target** is missing (unlabelled) or the row is invalid (corrupt record).
- Drop columns that are missing > ~90-95% and whose missingness indicator adds no CV lift, or that will not exist at serving time.
- Otherwise impute inside the Pipeline (fit on training folds) and add `add_indicator=True`, or use a model with native NaN support.

## Statistical inference (not just prediction)
For coefficient estimates and standard errors, single imputation understates uncertainty; use multiple imputation (MICE, Rubin's rules: `statsmodels.imputation.mice`) or full-information maximum likelihood.

## Test the choice
Cross-validate alternatives inside Pipelines: deletion (only where valid), simple imputation + indicator, iterative imputation, native NaN handling. Evaluate on a test set that keeps its missing values as production would.
