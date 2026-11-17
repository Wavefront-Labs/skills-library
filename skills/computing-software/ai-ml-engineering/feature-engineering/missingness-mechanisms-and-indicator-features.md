---
id: computing-software.ai-ml-engineering.feature-engineering.missingness-mechanisms-and-indicator-features
name: missingness-mechanisms-and-indicator-features
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, missing-data, missingness-mechanisms, mcar, mar, mnar, missing-indicator, missingno]
level: practitioner
status: gated
description: "Diagnose why values are missing (MCAR, MAR, MNAR) with missingness profiling and predictive checks, and keep the signal with indicator features and explicit missing categories."
sources:
  - https://academic.oup.com/biomet/article/63/3/581/270932
  - https://stefvanbuuren.name/fimd/sec-MCAR.html
  - https://github.com/ResidentMario/missingno
  - https://scikit-learn.org/stable/modules/impute.html#marking-imputed-values
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Missingness mechanisms and indicator features

**Goal:** understand the cause of missing values before choosing how to handle them, because the cause decides whether imputation is harmless, biased, or throwing away signal.

## The three mechanisms (Rubin, 1976 (gated: unconfirmed, source is paywalled or blocked))
- **MCAR** (missing completely at random): missingness unrelated to anything - e.g. a random sensor dropout. Dropping or simple imputation is unbiased (just less data).
- **MAR** (missing at random given observed data): depends on other observed variables - e.g. income missing more for younger users. Imputation conditioned on those variables (iterative/model-based) works.
- **MNAR** (missing not at random): depends on the missing value itself - e.g. high earners skip the income question, sick patients miss follow-ups. No imputation from observed data fixes it; the missingness *is* information.

## Diagnose
```python
import missingno as msno
msno.matrix(df); msno.heatmap(df)            # patterns and co-missingness between columns
miss = df.isna()
miss.mean().sort_values(ascending=False)       # rate per column
# does missingness depend on other variables / on the target?
for c in cols_with_missing:
    print(c, df.groupby(miss[c])["target"].mean().to_dict())
```
- If the target rate differs strongly between missing and present rows, missingness is predictive - keep it as a feature.
- Fit a classifier predicting `isna(col)` from other columns; AUC well above 0.5 rules out MCAR (consistent with MAR or MNAR).
- MNAR can't be proven from data alone; use domain knowledge (how was the form filled, when is the field written, which systems drop it).
- Check time: missing rates that change at a date usually mean a pipeline or form change, not a behaviour change.

## Structural vs true missing
"No previous loans" stored as NULL is not unknown - it's zero/none. Fix those with domain rules before generic imputation.

## Keep the signal
```python
SimpleImputer(strategy="median", add_indicator=True)            # numeric: value + is_missing flag
SimpleImputer(strategy="constant", fill_value="__missing__")   # categorical: its own category
```
Gradient boosting with native NaN handling learns the missing-value branch directly.

## Production check
The serving path must produce the same missingness as training (NULL vs empty string vs 0 vs default value from an API). A field that is never missing in production because the API fills a default silently shifts the model.

## Verify
- [ ] Missingness profile and suspected mechanism documented per important column.
- [ ] Structural missing values recoded with domain rules.
- [ ] Indicator features or missing categories kept where missingness is predictive.
