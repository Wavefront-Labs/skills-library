---
id: mathematics.applied-data-analysis-and-visualization.exploratory-data-analysis.first-pass-eda-workflow
name: first-pass-eda-workflow
category: mathematics
field: applied-data-analysis-and-visualization
product: exploratory-data-analysis
tags: [exploratory-data-analysis, eda, data-exploration, data-profiling, histogram, boxplot, scatterplot, pairs-plot, scatter-matrix, correlation, spearman, outliers, iqr, distribution, skew, log-transform, missingness, group-by, faceting, pandas, ydata-profiling, r, ggplot2, skimr, tidyverse, simpsons-paradox, anscombe, hypothesis-generation, data-analysis]
level: practitioner
status: verified
description: "A repeatable first pass over a new dataset: structure, univariate distributions, missingness, outliers, pairwise relationships and subgroup checks, written up as questions to test."
sources: ["Tukey, Exploratory Data Analysis (1977)", "Wickham, Çetinkaya-Rundel & Grolemund, R for Data Science (2e)", "pandas documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# First-pass EDA workflow

**Goal:** in an hour or two, know what a dataset contains, what is wrong with it, and
which questions are worth modelling — before any model gets fitted.

## 1. Structure (10 minutes)
- Rows, columns, types: pandas `df.shape`, `df.dtypes`, `df.head()`, `df.sample(10)`;
  R `dplyr::glimpse(df)`, `skimr::skim(df)`.
- **What is one row?** A customer, an order, a day? Check the supposed key is unique:
  `df['id'].is_unique` / `anyDuplicated(df$id)`. Most later errors come from a wrong
  answer here.
- Numbers stored as text (`"1,234"`, `"N/A"`), dates as strings, codes like zip/postcode
  read as integers (leading zeros lost). Fix types now.

## 2. One variable at a time
- Numeric: `df.describe()` plus a **histogram** with a few bin widths — one bin choice
  can hide bimodality. Look for spikes at 0, 999, -1, 1900-01-01 (sentinel values).
- Skewed positive data (income, sizes, durations): view on a log axis.
- Categorical: `value_counts(dropna=False)` — reveals typos ("NSW", "nsw", "N.S.W."),
  rare levels and how much is missing.
- Dates: count per day/month; gaps and sudden level shifts often mean a system change,
  not real behaviour.

## 3. Missingness
- Fraction missing per column, and **whether missingness depends on other columns**
  (e.g. missing income concentrated in one region). Cross-tab `isna()` against key
  groups. Missing not at random changes every downstream conclusion.

## 4. Outliers
- Flag with IQR fences (Q1 − 1.5·IQR, Q3 + 1.5·IQR) or robust z-scores
  (median/MAD). Then **look at the rows**: data error (fix/remove, document) or real
  extreme (keep; maybe it is the story). Never delete outliers just to tidy a plot.

## 5. Relationships
- Scatter-plot matrix for a handful of numeric columns (`pd.plotting.scatter_matrix`,
  `GGally::ggpairs`); use transparency or hexbin for many points.
- Correlations: Pearson for linear, **Spearman** for monotone/outlier-prone. Always plot —
  Anscombe's quartet has identical r ≈ 0.82 with four completely different shapes.
- Numeric vs category: box/violin plots per group with group sizes shown.

## 6. Subgroups and time
- Repeat key summaries split by the main grouping variables and by time period.
  An overall trend that reverses within every subgroup is **Simpson's paradox** — usually
  a mix-of-groups effect.
- Facet plots (`sns.relplot(col=…)`, `facet_wrap`) beat one cluttered chart.

## 7. Write it down
End with a short log: data issues found (and what you did), surprising patterns,
**questions/hypotheses to test** with fresh or held-out data. Patterns you found by looking
are hypotheses, not findings — testing them on the same data inflates false positives.
Automated profilers (`ydata-profiling`, `skimr`) are good for step 1–3 coverage, not
a substitute for steps 4–7.

## Uncertainty notes
The pandas calls above were run on pandas 3.x (`is_unique`, `value_counts(dropna=False)`,
`scatter_matrix`); `sns.relplot(col=...)` is in the seaborn reference; PyPI marks `pandas-profiling` deprecated in favour of
`ydata-profiling`. Anscombe's four correlations recomputed: 0.816, 0.816, 0.816, 0.817. The 1.5·IQR rule is a
convention, not a statistical test.

## Verify
- [ ] You can state what one row represents and the key is unique.
- [ ] Every column has a correct type; sentinel values identified.
- [ ] Missingness quantified and checked for dependence on other variables.
- [ ] Every flagged outlier was inspected and the decision recorded.
- [ ] Main relationships plotted (not just correlated) and checked within subgroups.
- [ ] Findings logged as hypotheses for confirmatory analysis.
