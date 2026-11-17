---
id: mathematics.applied-data-analysis-and-visualization.data-cleaning-and-preparation.missing-values-joins-and-validation
name: missing-values-joins-and-validation
category: mathematics
field: applied-data-analysis-and-visualization
product: data-cleaning-and-preparation
tags: [data-cleaning-and-preparation, data-cleaning, data-wrangling, data-preparation, missing-data, mcar, mar, mnar, imputation, multiple-imputation, listwise-deletion, deduplication, record-linkage, joins, merge, left-join, many-to-many, fan-out, reshape, pivot-longer, melt, tidy-data, validation, assertions, pandera, great-expectations, pointblank, cleaning-log, reproducibility, pandas, dplyr, data-analysis]
level: practitioner
status: verified
description: "Make a dataset analysable without silently corrupting it: missing-data handling by mechanism, safe joins that check row counts, reshaping to tidy form, validation rules and a cleaning log."
sources: ["Wickham, Tidy Data, Journal of Statistical Software (2014)", "van Buuren, Flexible Imputation of Missing Data (2e)", "pandas merge documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Missing values, joins and validation

**Goal:** a clean, analysis-ready table plus a scripted, re-runnable record of every
change — so the cleaning can be checked and repeated when new data arrives.

## 0. Ground rules
- **Never edit the raw file.** Read raw → script → write cleaned output. Every change
  lives in code (or at minimum a dated cleaning log).
- Count rows at every step. Unexplained row-count changes are the most common silent bug.

## 1. Missing values — decide by mechanism, not habit
- Standardise first: `""`, `"NA"`, `"n/a"`, `-999`, `0` used as "unknown" → real missing
  (`pd.NA`/`NaN`, R `NA`). Read with `na_values=[...]` explicitly.
- Ask *why* it is missing:
  - **MCAR** (unrelated to anything): complete-case analysis is unbiased, just less precise.
  - **MAR** (depends on observed variables): use **multiple imputation** (R `mice`,
    scikit-learn `IterativeImputer` with care) conditioning on those variables.
  - **MNAR** (depends on the missing value itself, e.g. high earners skip income):
    no method fixes it from the data alone — do a sensitivity analysis and say so.
- Mean/median imputation shrinks variance and distorts correlations; fine for a quick
  look, not for inference. Add a "was missing" indicator if you impute for prediction.
- Report how many rows each choice affects.

## 2. Inconsistencies and duplicates
- Trim whitespace, unify case, map variants to canonical codes with an explicit lookup
  table (keep it in version control), parse dates with a stated format
  (`pd.to_datetime(s, format="%d/%m/%Y")`) — day/month swaps are silent otherwise.
- Units: convert to one unit and note it (kg vs lb, cents vs dollars).
- Duplicates: exact (`df.duplicated()`), and **near** duplicates on a business key
  (same person, slightly different name). Decide which record wins and why.

## 3. Joins without fan-out
Before joining, know each side's key cardinality.
- pandas: `left.merge(right, on="id", how="left", validate="many_to_one", indicator=True)`
  — `validate` raises if the right side has duplicate keys; `_merge` shows unmatched rows.
- dplyr (1.1+): `left_join(x, y, by = "id", relationship = "many-to-one", unmatched = "error")`.
- Check: left-join row count = left row count; inspect unmatched keys (type mismatch
  "007" vs 7, trailing spaces, case).
- An accidental many-to-many join multiplies rows and inflates every sum afterwards.

## 4. Reshape to tidy form
One variable per column, one observation per row, one observational unit per table.
Wide → long: `df.melt(id_vars=..., var_name=..., value_name=...)` / `pivot_longer()`;
long → wide: `pivot` / `pivot_wider()` (pandas `pivot` raises `ValueError: Index contains
duplicate entries`; tidyr `pivot_wider()` instead warns and returns list-columns; use
`pivot_table` / `values_fn` to aggregate deliberately — duplicates are a signal, not an annoyance).

## 5. Validate in code
Write rules that fail loudly, and run them every time:
- Key unique, required columns non-null, ranges (age 0–120), allowed category sets,
  cross-field logic (end ≥ start), row count within expected bounds, totals reconcile
  with a source report.
- Tools: plain `assert` statements; `pandera` schemas (Python); `pointblank` or
  `validate` (R); Great Expectations for pipelines.

## 6. Document
Cleaning log: each step, rows affected, reason, who decided. Keep the script, raw data
hash/version and output together so the result is reproducible.

## Uncertainty notes
`validate=` and `indicator=` in pandas merge (both run here on pandas 3.x: `MergeError` on a
duplicate right key) and `relationship=`/`unmatched=` in dplyr joins (dplyr 1.1.0 NEWS) are
documented in the current reference pages; check the minimum version for older installs.
`IterativeImputer` needs `from sklearn.experimental import enable_iterative_imputer`.
Imputation choices for formal inference deserve a statistician's review.

## Verify
- [ ] Raw data untouched; all changes scripted and re-runnable.
- [ ] Missing-value codes standardised; mechanism assessed and treatment justified.
- [ ] Every join validated for cardinality and row count; unmatched keys inspected.
- [ ] Validation rules pass on the final table and totals reconcile with a known source.
- [ ] Cleaning log lists each change with rows affected.
