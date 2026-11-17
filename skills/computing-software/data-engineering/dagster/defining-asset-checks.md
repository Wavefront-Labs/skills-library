---
id: computing-software.data-engineering.dagster.defining-asset-checks
name: defining-asset-checks
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, asset-check, multi-asset-check, data-quality, asset-checks, definitions]
level: practitioner
status: docs-checked
description: "Define Dagster asset checks with @asset_check and @multi_asset_check, build them with a factory, and register them in Definitions."
sources:
  - https://docs.dagster.io/guides/test/asset-checks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Defining asset checks

Goal: test one property of an asset (no nulls in a column, schema adherence, freshness).

Keep each check to a single property. Asset checks do not count toward Dagster+ credit usage.

## Steps
1. Define with `@asset_check` (single) or `@multi_asset_check` (several run in one operation after the asset materializes). Docs example: fail if `order_id` contains null; the multi example also checks `item_id`.
2. Pass the checks to `Definitions`; otherwise Dagster does not see them.
3. Execution: by default jobs targeting an asset also run its checks; checks can also be run from the UI.
4. Results appear in the UI, customizable with metadata and severity levels.
5. Alerting on failed checks requires Dagster+.

A factory function can generate the checks for a `@multi_asset_check`. The dagster-dbt integration can model dbt tests as asset checks.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/test/asset-checks

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
