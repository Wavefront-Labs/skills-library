---
id: computing-software.data-engineering.dbt.pre-commit-hooks-for-dbt
name: pre-commit-hooks-for-dbt
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-checkpoint, pre-commit, sqlfluff, dbt-project-structure, code-quality, ci-checks, governance]
level: practitioner
status: docs-checked
description: "Enforce dbt project standards before merge with pre-commit: dbt-checkpoint hooks (descriptions, tests, owners), SQLFluff linting and YAML checks, locally and in CI."
sources:
  - https://github.com/dbt-checkpoint/dbt-checkpoint
  - https://pre-commit.com/
  - https://docs.sqlfluff.com/en/stable/usage/pre-commit
  - https://github.com/pre-commit/pre-commit-hooks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pre-commit hooks for dbt

**Goal:** every PR meets the project's rules (documented, tested, linted) automatically, so review time goes to logic.

## .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: <tag>
    hooks:
      - id: check-yaml
        args: [--unsafe]           # dbt YAML may contain jinja
      - id: end-of-file-fixer
      - id: trailing-whitespace
  - repo: https://github.com/sqlfluff/sqlfluff
    rev: <tag>
    hooks:
      - id: sqlfluff-lint
        additional_dependencies: ['<dbt-adapter>', 'sqlfluff-templater-dbt']
  - repo: https://github.com/dbt-checkpoint/dbt-checkpoint
    rev: <tag>
    hooks:
      - id: dbt-parse                       # refresh manifest.json
      - id: check-model-has-description
      - id: check-model-has-tests
      - id: check-model-columns-have-desc
        files: ^models/marts/
      - id: check-model-has-meta-keys
      - id: check-source-has-freshness
      - id: check-script-has-no-table-name   # no hard-coded tables, use ref/source
```
Replace each `<tag>` with a released tag from that repo and pin it; keep the adapter aligned with the project.

## How dbt-checkpoint works
Most hooks need `manifest.json` in the `target` folder, which is usually git-ignored, so run `dbt-parse` first in the hook list to generate it. Parsing needs a `profiles.yml`; supply secrets through CI secrets.

## Run
```bash
pip install pre-commit && pre-commit install
pre-commit run --all-files          # baseline whole repo
```
CI (GitHub Actions):
```yaml
- uses: actions/setup-python@v5
  with: {python-version: '3.11'}
- run: pip install pre-commit <dbt-adapter>
- run: dbt deps && pre-commit run --from-ref origin/main --to-ref HEAD
```

## Rollout on an existing project
Enable checks for new/changed files only, folder by folder (`files:` regex), rather than failing on hundreds of legacy models at once.

## Gotchas
- SQLFluff with the dbt templater needs a working profile and compiles models: slow on big projects. Use the `jinja` templater for speed with some accuracy loss, or lint only changed files.
- Contributors bypass with `--no-verify`; CI must run the same hooks.

## Verify
- [ ] A PR adding an undocumented model fails CI with a dbt-checkpoint message.
- [ ] `pre-commit run --all-files` passes on main.

## Checked
2026-11-01. Confirmed against the dbt-checkpoint README, pre-commit-hooks README and SQLFluff pre-commit page: hook ids (`dbt-parse`, `check-model-has-description`, `check-model-has-tests`, `check-model-columns-have-desc`, `check-model-has-meta-keys`, `check-source-has-freshness`, `check-script-has-no-table-name`, `sqlfluff-lint`, `check-yaml` with `--unsafe`), manifest.json in target needing `dbt-parse`, `additional_dependencies` for the dbt templater. Removed: pinned `rev` and adapter versions, hook argument examples, catalog.json claim, changed-files-only claim, `DBT_PROFILES_DIR` example.
Method: documentation only; no commands were run.
