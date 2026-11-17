---
id: computing-software.data-engineering.databricks.bundle-bind-and-generate
name: bundle-bind-and-generate
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-asset-bundles, bundle-bind, bundle-generate, import-existing-jobs, unbind, migration-to-bundles]
level: practitioner
status: docs-checked
description: "Bring UI-created Databricks jobs, pipelines and dashboards under Asset Bundles with bundle generate and deployment bind, updating the existing resources in place."
sources:
  - https://docs.databricks.com/en/dev-tools/bundles/migrate-resources.html
  - https://docs.databricks.com/en/dev-tools/cli/bundle-commands.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bundle generate and bind

**Goal:** convert click-ops jobs into version-controlled bundle resources while updating the existing resources in place (same job ID, so external references keep working).

## 1. Generate YAML from an existing resource
```bash
databricks bundle generate job --existing-job-id 123456 --key sales_daily -t prod
databricks bundle generate pipeline --existing-pipeline-id 9a8b-... --key sales_pipeline
databricks bundle generate dashboard --existing-id 01ef... --key exec_kpis
```
Creates the resource configuration file in the bundle's `resources` folder and downloads referenced artifacts into `src`. Adding `--bind` binds the resource right after generation. Review: remove hard-coded cluster IDs, parameterise catalog names with `${var.catalog}`, and replace user paths.

## 2. Bind the bundle resource to the existing object
```bash
databricks bundle deployment bind sales_daily 123456 -t prod
databricks bundle deploy -t prod
```
After binding, `deploy` **updates** job 123456 in place instead of creating a new job. The bundle now owns its configuration: manual UI edits will be overwritten on the next deploy.

## 3. Unbind (hand back or retire)
```bash
databricks bundle deployment unbind sales_daily -t prod
```
This removes the link between the bundle resource and its counterpart in the workspace.

## Migration checklist
- Pause the job's schedule during the switch if the generated config differs materially.
- Compare the job settings in the workspace before and after the first deploy to confirm only intended changes.
- Keep `run_as` and permissions identical to avoid breaking access.
- Notebooks moved from `/Workspace/Users/...` to bundle paths: update any relative notebook paths.
- External callers (Airflow, ADF) keep using the same job ID because it did not change.

## Gotchas
- Run bind with `--target`, and confirm the resource in the workspace first. Bind does not recreate data: a bound pipeline keeps its existing data.
- `generate` captures current UI state, including oddities (personal clusters, deprecated runtimes). Clean up before committing.

## Verify
- [ ] `databricks bundle summary -t prod` lists the resource with the original ID.
- [ ] The first deploy updates the existing job rather than creating a new one.

## Checked
2026-10-28 Confirmed on the Databricks CLI bundle commands page and the migrate-resources page: `bundle generate job --existing-job-id`, `--key`, `--bind`, `generate pipeline --existing-pipeline-id`, `generate dashboard --existing-id`, `bundle deployment bind KEY RESOURCE_ID` used with `--target`, `bundle deployment unbind KEY`, bind updates the existing resource and does not recreate data, generate writes to the resources folder and downloads artifacts to src, `bundle summary`. Removed (not on the fetched pages): run-history guarantee, `databricks jobs get` command, `%run`/`dbutils.notebook.run` note, the claims about destroy after unbind, dev-target copies and deletion when a bound resource is removed from YAML.
Method: documentation only; no commands were run.
