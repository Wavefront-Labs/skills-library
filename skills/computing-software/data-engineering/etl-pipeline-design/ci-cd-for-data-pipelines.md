---
id: computing-software.data-engineering.etl-pipeline-design.ci-cd-for-data-pipelines
name: ci-cd-for-data-pipelines
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, data-pipeline-cicd, ci-cd, slim-ci, deployment]
level: advanced
status: docs-checked
description: "Build CI/CD for data pipelines: lint and unit tests, PR builds against isolated schemas, modified-only runs with deferral, data diffs, and promotion to production."
sources:
  - https://docs.getdbt.com/docs/deploy/continuous-integration
  - https://docs.databricks.com/aws/en/dev-tools/ci-cd/
  - https://docs.github.com/en/actions
  - https://docs.getdbt.com/reference/node-selection/defer
  - https://docs.getdbt.com/reference/node-selection/methods
  - https://docs.databricks.com/aws/en/dev-tools/cli/bundle-commands
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CI/CD for data pipelines

**Goal:** every change to SQL/Python pipelines is tested on real data structures before merge and deployed reproducibly.

## CI on pull request
1. **Static**: SQL lint (sqlfluff), Python lint/type check (ruff, mypy), YAML/schema validation, orchestrator DAG import tests.
2. **Unit**: Python transforms with small fixtures (pytest), UDF tests.
3. **Build in isolation**: PR-specific schema/database (`pr_1234`), deferral to prod artifacts for unchanged upstreams (`--defer` needs a manifest from a previous run, passed with `--state`):
```bash
dbt build --select state:modified+ --defer --state prod-artifacts/
```
4. **Data checks**: data tests on built models; data diff of modified models vs prod (row counts, changed rows, column stats).
5. **Teardown**: drop PR schemas on merge/close.

## CD
- Artifact = commit SHA (image tag, wheel version, bundle); same artifact promoted dev -> staging -> prod.
- Deploy tools: dbt Cloud jobs or `dbt build` in the orchestrator image, `databricks bundle deploy -t prod` (`-t`/`--target` selects the bundle target), and your infrastructure-as-code tool.
- Run-as service principals; secrets from the CI secret store, never committed.
- Post-deploy smoke run of critical pipelines, or the next scheduled run monitored closely.

## GitHub Actions sketch
```yaml
on: pull_request
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt && dbt deps
      - run: sqlfluff lint models/
      - run: aws s3 cp s3://acme-dbt-artifacts/prod/manifest.json prod-artifacts/   # or dbt Cloud API
      - run: dbt build --select state:modified+ --defer --state prod-artifacts
        env: {DBT_SCHEMA: "pr_${{ github.event.number }}"}
```

## Gotchas
- CI that builds everything every time gets slow and skipped; use modified-only selection.
- Stale prod artifacts make `state:modified` select too much/little; publish artifacts on every prod run.
- Schema changes to large incremental tables need explicit migration steps (full refresh or on_schema_change), not just a deploy.

## Verify
A PR introducing a broken join fails CI on a data test or diff; merged changes reach prod only through the pipeline.

## Checked

2026-10-28. Confirmed in the dbt defer and node-selection methods pages: `--defer` requires a manifest from a previous invocation passed with `--state`, and `state:modified` selects new and changed nodes. Confirmed in the Databricks CLI bundle commands page: `databricks bundle deploy` with `-t`/`--target`. Removed: `--target ci` on the dbt commands, dbt unit tests, zero-copy clones, the `snow` CLI and OIDC federation claims (not confirmed in the cited pages).

Method: documentation only; no commands were run.
