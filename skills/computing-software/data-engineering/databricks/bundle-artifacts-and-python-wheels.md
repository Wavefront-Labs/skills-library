---
id: computing-software.data-engineering.databricks.bundle-artifacts-and-python-wheels
name: bundle-artifacts-and-python-wheels
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, bundle-artifacts, python-wheel, asset-bundles, packaging]
level: advanced
status: docs-checked
description: "Build and deploy Python wheels with Databricks Asset Bundles: the artifacts mapping, a build command, python_wheel_task and the libraries reference."
sources:
  - https://docs.databricks.com/aws/en/dev-tools/bundles/settings#artifacts
  - https://docs.databricks.com/aws/en/dev-tools/bundles/python-wheel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bundle artifacts and Python wheels

**Goal:** package shared code as a wheel, built by the bundle and used by jobs without manual uploads.

## Config
```yaml
artifacts:
  default:
    type: whl
    build: poetry build            # the docs also show python3 setup.py bdist wheel
    path: .

resources:
  jobs:
    etl:
      tasks:
        - task_key: main
          python_wheel_task:
            package_name: my_package
            entry_point: main
          libraries:
            - whl: ./dist/*.whl
```
- `artifacts` maps an artifact name to `type: whl` and a `build` command; `path` is the folder the build runs in.
- `python_wheel_task` takes `package_name` and `entry_point`; the entry point is declared in the package's own metadata (the docs show `entry_points` in `setup.py`).
- `libraries` with `whl: ./dist/*.whl` points the task at the built wheel.
- Deploy from the bundle root with `databricks bundle deploy --target dev`; the settings page documents `workspace.artifact_path` as the place artifacts are uploaded.

## Gotchas
- A glob on `./dist/*.whl` picks every wheel in `dist/`, so keep stale builds out of that folder.

## Verify
The `databricks bundle deploy` output shows the build and upload, and the job run uses the wheel.

## Checked
2026-11-01. Confirmed against the Databricks pages Bundle settings (artifacts) and Develop a Python wheel file using Databricks Asset Bundles (type whl, build, python_wheel_task, package_name, entry_point, whl library glob, bundle deploy). Removed: the uv build command, pyproject.toml example, the version patching and cluster caching claims, and the serverless environment_key claim.
Method: documentation only; no commands were run.
