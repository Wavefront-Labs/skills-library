---
id: computing-software.data-engineering.dbt.project-evaluator-best-practice-checks
name: project-evaluator-best-practice-checks
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, project-evaluator-rules, dbt-project-evaluator, governance, linting]
level: practitioner
status: gated
description: "Enforce dbt project best practices with dbt_project_evaluator: DAG, testing, documentation, structure and performance rules, exceptions, coverage targets and CI wiring."
sources:
  - https://dbt-labs.github.io/dbt-project-evaluator/latest/
  - https://hub.getdbt.com/dbt-labs/dbt_project_evaluator/latest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dbt_project_evaluator

**Goal:** catch modelling smells (direct joins to sources, fanout, missing PK tests, undocumented models) automatically in CI.

## Install
```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_project_evaluator
    version: [">=1.0.0", "<2.0.0"]
```
```bash
dbt deps
dbt build --select package:dbt_project_evaluator
```
Each rule is a model `fct_*` plus a test; failing rows name the offending nodes. (gated: unconfirmed, source is paywalled or blocked)

## Rule families (examples)
- Modelling: `fct_direct_join_to_source`, `fct_rejoining_of_upstream_concepts`, `fct_model_fanout`, `fct_staging_dependent_on_staging`, `fct_root_models`, `fct_hard_coded_references`.
- Testing: `fct_missing_primary_key_tests`, `fct_test_coverage`.
- Documentation: `fct_undocumented_models`, `fct_documentation_coverage`.
- Structure: `fct_model_naming_conventions`, `fct_model_directories`, `fct_source_directories`.
- Performance: `fct_chained_views_dependencies`, `fct_exposure_parents_materializations`.
- Governance: `fct_public_models_without_contract`, `fct_undocumented_public_models`.

## Tune
```yaml
# dbt_project.yml
vars:
  dbt_project_evaluator:
    test_coverage_target: 100
    documentation_coverage_target: 100
    models_fanout_threshold: 3
models:
  dbt_project_evaluator:
    marts:
      dag:
        fct_model_fanout:
          +enabled: false
```
Exceptions: seed `dbt_project_evaluator_exceptions.csv` (fct_name, column_name, id_to_exclude, comment) in your project and disable the package's own seed.

## CI
Run after `dbt parse` on the PR; fail the job on errors. On large projects run nightly instead of per PR if runtime matters.

## Gotchas
- It builds models in your warehouse (small); give it its own schema.
- Some rules need naming conventions configured (`model_types`, prefixes) to match your project.

## Verify
Introduce a model selecting directly from a source in marts: `fct_direct_join_to_source` test fails.

## Checked

2026-11-02

- Confirmed: The dbt_project_evaluator docs home page and its dbt Hub page were fetched.
- Removed or gated: Only the home page was readable; the individual fct_* rule names, the *_target variable names and the exceptions seed layout live on rule sub-pages that were not fetched; gated, confirm in the package documentation.

Method: documentation only; no commands were run.
