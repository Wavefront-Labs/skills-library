---
id: computing-software.data-engineering.dbt.advanced-ci-compare-changes
name: advanced-ci-compare-changes
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, advanced-ci-compare, dbt-cloud, data-diff, ci-jobs]
level: advanced
status: docs-checked
description: "Use dbt Cloud Advanced CI compare changes to see row, column and primary-key level diffs of a PR build against production before merging."
sources:
  - https://docs.getdbt.com/docs/deploy/advanced-ci
  - https://docs.getdbt.com/docs/deploy/ci-jobs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Advanced CI: compare changes

**Goal:** reviewers see what a model change does to data (rows added/removed/changed, column changes) not only that it builds.

## What it does
In a dbt Cloud CI job with **dbt compare** enabled, dbt compares the last applied production state with the pull request changes whenever the PR is opened or new commits are pushed, and reports:
- changes to the data primary keys, rows and columns (Compare tab of the job run)
Results show in the Compare tab of the job run and as a summary comment on the pull request.

## Setup
1. A dbt platform Enterprise or Enterprise+ account with Advanced CI features enabled, on BigQuery, Databricks, Postgres, Redshift or Snowflake.
2. CI job: deferral to the production environment (default), with the default command `dbt build --select state:modified+`.
3. Enable the **dbt compare** option in the CI job settings.
4. Set `event_time` on models so comparisons use only the time range present in both CI and production; otherwise a CI build of a data subset shows the missing rows as deleted.

## Cost control
Compare queries run in the CI job's environment against both the CI and the production relation. The compare command can be customised (for example `--exclude` large models) in the CI job settings.



## Gotchas
- CI and production relations must live on the same database host/connection; if the CI job defers to a production job on a different host, compare changes does not work.
- Comparison results are cached (at most 100 records per modified model) for up to 30 days; older runs show an expired-data message.

## Verify
Open a PR that changes a model: the Compare tab in the job run and the PR comment show primary-key, row and column changes against production.

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: Advanced CI requires Enterprise or Enterprise+ and supported platforms (BigQuery, Databricks, Postgres, Redshift, Snowflake); the dbt compare option and default CI command; results appear in the Compare tab and as a PR comment; `event_time` overlap behaviour; cache limit of 100 records per model for up to 30 days; same-host requirement; `--exclude` customisation. Removed unconfirmed claims about primary-key requirements, sampling options and third-party diff tools.

Method: documentation only; no commands were run.
