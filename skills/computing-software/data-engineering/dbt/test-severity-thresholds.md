---
id: computing-software.data-engineering.dbt.test-severity-thresholds
name: test-severity-thresholds
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, warn-if-error-if, test-severity, data-tests, store-failures]
level: practitioner
status: verified
description: "Tune dbt data test outcomes with severity, warn_if and error_if thresholds, where filters and limits, so known noise warns while real breakage fails builds."
sources:
  - https://docs.getdbt.com/reference/resource-configs/severity
  - https://docs.getdbt.com/reference/resource-configs/where
  - https://docs.getdbt.com/reference/resource-configs/store_failures
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# warn_if / error_if thresholds

**Goal:** tests that fail only when a problem matters, warn on tolerable noise, and never get disabled out of frustration.

## Config
```yaml
columns:
  - name: email
    data_tests:
      - not_null:
          config:
            severity: error
            error_if: ">100"
            warn_if: ">0"
            where: "created_at >= dateadd('day', -3, current_date)"
            store_failures: true
```
- A test query returns failing rows; the **count** is compared to the conditions.
- Defaults: `severity: error`, `error_if: "!= 0"`, `warn_if: "!= 0"`.
- Logic: with `severity: error`, error_if is checked first, then warn_if. With `severity: warn`, only warn_if is evaluated: it can never error.
- Expressions: SQL-style comparisons against the integer failure count (`>`, `>=`, `!=`, `=`; the docs also show `between 5 and 10`). No percentages: for ratios write a singular test returning one row when the ratio is breached.

## Project-wide defaults
```yaml
# dbt_project.yml
data_tests:
  my_project:
    +severity: warn            # e.g. for a legacy folder
    marts:
      +severity: error
```

## Tips
- `where` limits to recent data so historic garbage does not fail forever (pair with a one-off cleanup).
- `limit: 1000` caps failing rows stored/returned.
- `store_failures: true` (or `+store_failures_as: view`) writes failing rows to `<schema>_dbt_test__audit` for triage.
- Use `dbt build --warn-error-options '{"error": ["NoNodesForSelectionCriteria"]}'` style flags for warnings policy (on 1.12.6 the `include` key is rejected: "Please use `error`"), not to promote test warnings wholesale. `--warn-error` turned a test warning into a failing exit code 1.

## Verify
`dbt test --select <model>` shows WARN vs ERROR as expected for seeded bad rows below and above the threshold (checked: 1 orphan row gave `WARN 1`, 150 gave `FAIL 150` with `warn_if: ">0"`, `error_if: ">100"`).
