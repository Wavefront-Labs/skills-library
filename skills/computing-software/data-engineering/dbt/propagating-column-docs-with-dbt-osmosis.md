---
id: computing-software.data-engineering.dbt.propagating-column-docs-with-dbt-osmosis
name: propagating-column-docs-with-dbt-osmosis
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-osmosis, documentation, column-descriptions, yaml-management]
level: practitioner
status: docs-checked
description: "Propagate dbt column descriptions downstream and keep YAML files organised with dbt-osmosis: config, yaml refactor/document/organize, dry runs and CI checks."
sources:
  - https://github.com/z3z1ma/dbt-osmosis
  - https://z3z1ma.github.io/dbt-osmosis/
  - https://z3z1ma.github.io/dbt-osmosis/docs/reference/cli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Propagating column docs (dbt-osmosis)

**Goal:** document a column once (in staging) and have the same description flow to every downstream model that passes it through.

## Install
```bash
pip install dbt-osmosis      # same env as dbt
```

## Declare where YAML lives
```yaml
# dbt_project.yml
models:
  my_project:
    +dbt-osmosis: "_{parent}.yml"     # one file per folder, named after the folder
    staging:
      +dbt-osmosis: "{model}.yml"     # or one file per model
```
Context variables such as `{model}`, `{node}` and `{parent}` decide the target file; per-folder behaviour can be tuned with `+dbt-osmosis-options` (for example `skip-add-columns: true`).

## Commands
```bash
dbt-osmosis yaml organize          # move/create YAML blocks to match the declared layout
dbt-osmosis yaml document          # column documentation inheritance, optional column injection/sorting
dbt-osmosis yaml refactor          # organize + document
dbt-osmosis yaml refactor --dry-run --check     # the README's check form (-C also works as a pre-commit hook)
dbt-osmosis yaml refactor --fqn marts.finance   # limit scope (-f, repeatable)
```
`--catalog-path` and `--disable-introspection` exist for controlling how column metadata is read; see the CLI reference.

## How inheritance works
`yaml document` applies column documentation inheritance from upstream models. Flags such as `--force-inherit-descriptions`, `--skip-merge-meta` and `--skip-add-tags` control what is inherited. Check the output on a sample model for any renamed columns.

## Gotchas
- It rewrites YAML files; run once, commit separately, then keep a check in CI to avoid noisy diffs.
- `--skip-add-columns` / `--skip-add-data-types` flags exist when you do not want every column listed.
- Review the first run: wrong upstream descriptions propagate just as well as right ones.

## Verify
After `document`, `dbt docs generate` shows inherited descriptions on mart columns; the check run in CI passes on a clean branch.

## Checked
2026-11-01. Confirmed in the dbt-osmosis repo (README, docs intro, CLI reference): `yaml organize|document|refactor`, `+dbt-osmosis` routing and `+dbt-osmosis-options`, `{model}`/`{parent}` context variables, `--dry-run`, `--check`/`-C`, `--fqn`/`-f`, `--skip-add-columns`, `--skip-add-data-types`, `pip install`, pre-commit use. Removed: `{node.schema}` template, the exit-code guarantee for `--check`, the target-connection requirement, and the step-by-step upstream-walk and rename-break description.
Method: documentation only; no commands were run.
