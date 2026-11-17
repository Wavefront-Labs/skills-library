---
id: computing-software.data-engineering.dagster.unit-testing-assets-and-ops
name: unit-testing-assets-and-ops
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, unit-test, pytest, build-asset-context, mock-resource, direct-invocation]
level: practitioner
status: docs-checked
description: "Unit test Dagster assets by invoking them directly with inputs, Config objects, mocked resources, build_asset_context, and a mock IO manager for multi-assets."
sources:
  - https://docs.dagster.io/guides/test/unit-testing-assets-and-ops
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Unit testing assets and ops

Goal: fast feedback by invoking computations directly with specified inputs and mocked resources. Unit tests cannot fully replace integration tests or manual review.

Guidance from the docs: testing individual assets is generally recommended over unit testing entire jobs; unit testing is not recommended where most business logic lives in an external system (for example an asset that directly invokes an external Databricks job); to test at runtime, use asset checks.

## Cases
- No arguments: invoke the definition directly.
- Upstream dependencies: pass a value for the dependency when invoking.
- Config: construct the required config object and pass it in.
- Resources: create a mock instance of the resource to avoid external services.
- Context argument: construct one with `build_asset_context()`.
- Multiple parameters: use keyword arguments for clarity.
- Multi-assets with upstream assets: you cannot use `input_values` (not designed for assets). Define standalone source assets and use a mock IO manager that returns test data based on the asset key being loaded.

## Run
From the top-level project directory (the one containing the tests directory): `pytest tests` (or your runner of choice).

## Checked
2026-11-08. Confirmed against the Dagster docs page Unit testing assets and ops (raw markdown from the docs repo): guidance notes, each case, multi-asset caveat, pytest command. Code snippets are referenced by file and were not read. Nothing removed.
Method: documentation only; no commands were run.
