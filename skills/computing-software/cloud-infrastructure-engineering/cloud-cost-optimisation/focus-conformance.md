---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.focus-conformance
name: focus-conformance
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-tools, focus-conformance, focus, finops-open-cost-and-usage-specification, billing-data]
level: practitioner
status: docs-checked
description: "Check a cost dataset against the FOCUS specification with the FinOps Foundation focus_validator: version, applicability criteria, report formats, CI use."
sources: ["https://focus.finops.org/", "https://github.com/finopsfoundation/focus_validator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FOCUS conformance with focus_validator

FOCUS is the FinOps Open Cost and Usage Specification. The FinOps Foundation `focus_validator` checks a cost and usage
dataset (CSV or Parquet) against a chosen FOCUS version. It loads rules from the specification, turns them into DuckDB
SQL and runs them against the data.

## Install
Python 3.9 or later and Poetry. Clone the repository, then `poetry install`.

## Run
```bash
poetry run focus-validator --data-file export.csv --validate-version 1.2 --applicability-criteria ALL --output-type web --output-destination report.html
```
- `--validate-version` picks the FOCUS version to check against; know which version each export claims.
- `--applicability-criteria ALL` includes rules that only apply when a provider supports a capability; the default runs
  only universally applicable rules. `--show-applicability-criteria` lists the criteria for a version.
- `--output-type`: `web` (interactive HTML, the README's recommended form), console (default text) or `unittest` (JUnit
  XML for CI, with `--output-destination results.xml`).
- Results show PASS, FAILED or SKIPPED per rule. Skipped rules are dynamic (need runtime data analysis) or not
  applicable to the criteria you chose.
- `--explain-mode` with `--focus-dataset CostAndUsage` prints every rule, its requirement text and SQL without needing data.

## Gotchas
- A CSV whose first 10,000 rows are mostly null can have column types mis-inferred (numbers read as strings); the README
  suggests explicit column types, cleaning the data, a longer inference length, or Parquet.
- Type-check failures often come from that inference problem rather than the export itself; check before blaming a provider.
- Run with `--applicability-criteria ALL` before declaring a column missing: a skipped rule is not a pass.

## Verify
- [ ] The validator version and FOCUS version used are recorded with the result.
- [ ] Failures are fixed upstream or listed as known gaps; skipped rules are reviewed, not read as passes.

## Checked
Confirmed against the focus_validator README: purpose, CSV and Parquet inputs, DuckDB engine, Python and Poetry
requirements, CLI flags and output types, applicability criteria behaviour, PASS/FAILED/SKIPPED results, explain mode,
schema inference caveat. Removed: spec version history and GA dates, the mandatory column list, ChargeCategory values,
Tags format, provider export names and gap statements, the `x_` column claim, reconciliation steps and vendor questions
(none read in an official page this batch).
Method: docs-checked 2026-11-09 against https://github.com/finopsfoundation/focus_validator README (raw) and https://focus.finops.org/
