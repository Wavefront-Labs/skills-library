---
id: computing-software.data-engineering.dbt.documentation-coverage-checks
name: documentation-coverage-checks
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, doc-coverage, dbt-coverage, documentation, ci-checks]
level: practitioner
status: docs-checked
description: "Measure and enforce dbt documentation and test coverage in CI with dbt-coverage, project evaluator coverage targets, and pre-commit description checks."
sources:
  - https://github.com/slidoapp/dbt-coverage
  - https://github.com/dbt-checkpoint/dbt-checkpoint
  - https://dbt-labs.github.io/dbt-project-evaluator/latest/rules/documentation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Documentation coverage checks

**Goal:** a number for "how much of the project is documented", and a gate that stops it falling.

## dbt-coverage
```bash
pip install dbt-coverage
dbt docs generate                     # generates catalog.json and manifest.json
dbt-coverage compute doc --cov-report coverage-doc.json --cov-fail-under 0.8   # fail below 80%
dbt-coverage compute test --cov-report coverage-test.json
dbt-coverage compute doc --cov-report after.json --cov-fail-compare before.json   # fail if coverage dropped vs before.json
dbt-coverage compare coverage-doc.json main-coverage-doc.json   # after.json first, before.json second
```
`compute` reads `target/catalog.json` and `target/manifest.json` and reports documented columns per table and in total. Scope with `--model-path-filter` (repeatable) or `--model-path-exclusion-filter`; `--cov-format markdown` prints a Markdown table.

## Project evaluator
`fct_documentation_coverage` calculates the percent of enabled models with a description and warns when it is below `documentation_coverage_target` (default 100%, overridable as a variable); `fct_undocumented_models` lists every model with no description.

## pre-commit (dbt-checkpoint)
```yaml
- repo: https://github.com/dbt-checkpoint/dbt-checkpoint
  rev: v2.0.10
  hooks:
    - id: check-model-has-description
    - id: check-model-columns-have-desc
```
## Policy
- Use `--cov-fail-under` for an absolute floor, or `--cov-fail-compare before.json` to block decreases without demanding an absolute number on legacy projects.

## Gotchas
- `dbt-coverage` needs `catalog.json`, so run `dbt docs generate` first.

## Verify
A PR adding a model without a description lowers the `dbt-coverage compare` result and fails the `--cov-fail-compare` check.

## Checked

2026-10-25: third-party READMEs and docs on GitHub. Confirmed: dbt-coverage README (repository last commit 2026-10-07, release v0.5.0): `compute doc|test`, `--cov-report`, `--cov-fail-under`, `--cov-fail-compare`, `--model-path-filter`, `compare after before`, inputs `catalog.json` and `manifest.json`; dbt-checkpoint hook ids `check-model-has-description` and `check-model-columns-have-desc` (latest release v2.0.10); dbt-project-evaluator documentation rules `fct_documentation_coverage` (target default 100%) and `fct_undocumented_models`. Removed unconfirmed policy advice and the dbt-osmosis claim.

Method: documentation only; no commands were run.
