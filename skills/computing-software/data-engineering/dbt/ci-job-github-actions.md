---
id: computing-software.data-engineering.dbt.ci-job-github-actions
name: ci-job-github-actions
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-ci-job, github-actions, slim-ci, pull-request-ci, ci-schema, sqlfluff, dbt-cloud-ci, pr-checks]
level: advanced
status: docs-checked
description: "Run dbt CI on pull requests: GitHub Actions with per-PR schemas, prod manifest download, state:modified+ build with defer, linting, schema cleanup; dbt Cloud equivalent."
sources:
  - https://docs.getdbt.com/docs/deploy/continuous-integration
  - https://docs.getdbt.com/best-practices/best-practice-workflows
  - https://docs.getdbt.com/reference/node-selection/defer
  - https://docs.github.com/actions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dbt CI job (GitHub Actions)

**Goal:** every PR proves its changed models compile, build and pass tests against real data before merge, in an isolated schema.

## Workflow
```yaml
# .github/workflows/dbt-ci.yml
name: dbt-ci
on: pull_request
jobs:
  build:
    runs-on: ubuntu-latest
    env:
      DBT_PROFILES_DIR: ./ci
      DBT_CI_SCHEMA: dbt_ci_pr_${{ github.event.number }}
      SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
      DBT_ENV_SECRET_SNOWFLAKE_PRIVATE_KEY: ${{ secrets.SNOWFLAKE_CI_KEY }}
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with: {python-version: "3.x"}
      - run: pip install -r requirements-dbt.txt        # pinned dbt-core + adapter
      - run: dbt deps
      - name: fetch prod manifest
        run: |
          mkdir -p prod-state
          aws s3 cp s3://<BUCKET>/dbt/prod-artifacts/manifest.json prod-state/manifest.json
      - run: dbt build -s state:modified+ --defer --state prod-state --target ci --fail-fast
      - if: always()
        uses: actions/upload-artifact@v7
        with: {name: dbt-target, path: target/}
```
`ci/profiles.yml` target `ci` uses `schema: "{{ env_var('DBT_CI_SCHEMA') }}"`; keep CI credentials separate from production ones.

## Publish the prod manifest
Upload the production run's `target/manifest.json` after every successful run so CI compares against current prod; `--state` points at the folder holding it.

## Cleanup
On PR close, run a `dbt run-operation` macro of your own that drops the `dbt_ci_pr_<n>` schema (separate workflow on `pull_request: types: [closed]`), plus a scheduled sweep for leftovers.

## dbt Cloud
CI jobs triggered by pull requests do the same automatically: a temporary schema unique to the PR (named `dbt_cloud_pr_<job_id>_<pr_id>`), builds and tests of affected models, and deletion of the temporary schema when the PR is merged or closed. The default job command is `dbt build --select state:modified+`, with deferral to a chosen environment (Production by default). Advanced CI adds compare changes (Enterprise tier). CI runs for different PRs execute concurrently; runs for the same PR execute serially and the latest commit wins.

## Extras worth adding
- dbt platform compare changes (Advanced CI) for data diffs of modified models against production.

## Verify
- [ ] A PR with a broken model fails the check; merge is blocked by branch protection.
- [ ] CI schemas disappear after PRs close.
- [ ] CI runtime stays proportional to the change size (Slim CI working).

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: dbt CI docs and node-selection docs: `dbt build -s state:modified+ --defer --state <dir> --fail-fast` flags, `DBT_ENV_SECRET_` prefix for secret env vars, dbt platform CI temporary schema prefix `dbt_cloud_pr_`, default CI command, deferral default, concurrency rules and teardown on merge or close. Action versions use the latest major tags from each repository releases (checkout v7, setup-python v7, upload-artifact v7). Removed unconfirmed sqlfluff, dbt-project-evaluator and dbt-checkpoint claims and the CI role description.

Method: documentation only; no commands were run.
