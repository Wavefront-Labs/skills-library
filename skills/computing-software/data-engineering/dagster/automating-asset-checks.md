---
id: computing-software.data-engineering.dagster.automating-asset-checks
name: automating-asset-checks
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, asset-checks, on-cron, eager, automation-condition, data-quality]
level: practitioner
status: docs-checked
description: "Automate Dagster asset check execution independently of assets using AutomationCondition.on_cron or eager."
sources:
  - https://docs.dagster.io/guides/automate/declarative-automation/automating-asset-checks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Automating asset checks

Attach automation conditions to asset checks to run data quality independently of the asset.

## on_cron
The check waits, from each cron tick, for its asset to update, then is requested once and not again until the next tick. Good for slow or expensive checks run less often than the asset updates. It is not requested if upstream assets do not all update within the tick.

## eager
The check runs whenever an upstream dependency updates. It is not requested if any upstream partition is unmaterialized, waits for in-progress upstream runs and for its own in-progress run. Observation counts as an update only if the data version changed; a materialization always counts.

Customization follows the on_cron and eager customization skills.

## Checked

2026-11-09. Pages read in full against this skill:
- https://docs.dagster.io/guides/automate/declarative-automation/automating-asset-checks

Confirmed: on_cron and eager behaviours, upstream/in-progress rules and the observation versus materialization update rule, against the page text.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
