---
id: computing-software.data-engineering.databricks.asset-bundle-project-structure
name: asset-bundle-project-structure
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-asset-bundles, databricks-yml, bundle-targets, bundle-variables, bundle-resources, include, presets, run-as, infrastructure-as-code]
level: practitioner
status: docs-checked
description: "Lay out a Databricks Asset Bundle: databricks.yml with targets, variables, include files, job/pipeline resources, dev-mode prefixes and run_as identities."
sources:
  - https://docs.databricks.com/aws/en/dev-tools/bundles/
  - https://docs.databricks.com/aws/en/dev-tools/bundles/settings
  - https://docs.databricks.com/aws/en/dev-tools/bundles/deployment-modes
  - https://docs.databricks.com/aws/en/dev-tools/bundles/variables
  - https://docs.databricks.com/aws/en/dev-tools/bundles/templates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Databricks Asset Bundle project structure

**Goal:** one repo describes code plus the jobs, pipelines and other workspace resources that run it, deployable to dev, staging and prod with only target-level differences.

## 1. Start from a template
```bash
databricks bundle init default-python
```
Keep the generated layout: a `databricks.yml` at the root (bundle name, includes, variables, targets) with resource definitions in separate YAML files pulled in through `include`, and source code alongside.

## 2. databricks.yml skeleton
```yaml
bundle:
  name: my_bundle

include:
  - resources/*.yml

variables:
  catalog:
    description: Target Unity Catalog catalog
    default: dev
  warehouse_id:
    lookup:
      warehouse: "<warehouse-name>"     # name resolved to the object's ID

targets:
  dev:
    mode: development
    default: true
    workspace:
      host: https://<workspace-host>
  prod:
    mode: production
    workspace:
      host: https://<workspace-host>
      root_path: /Workspace/Shared/.bundle/${bundle.name}/${bundle.target}
    variables:
      catalog: prod
    run_as:
      service_principal_name: <sp-application-id>
```

## 3. Rules that save pain
- Substitutions include `${bundle.target}`, `${bundle.name}`, `${workspace.current_user.short_name}` and `${var.<name>}`. Provide variable values with `--var="<key>=<value>"` on a bundle command, or with an environment variable whose name starts with `BUNDLE_VAR_`.
- `mode: development` prefixes non-file resources with `[dev ${workspace.current_user.short_name}]`, tags jobs and pipelines with a `dev` tag, and pauses all schedules and triggers. Customise this with `presets`; if both are set, presets override the mode defaults and settings on individual resources override presets.
- `mode: production` validates that the Git branch matches the target's `git.branch` if set (override with `--force`) and that Lakeflow pipelines are `development: false`. Databricks recommends service principals for production; set `run_as` to one.
- Never hard-code cluster IDs or catalog names in notebooks; pass a variable as a job parameter.

## Verify
- [ ] `databricks bundle validate` accepts the configuration (`--output json` shows resolved values).
- [ ] Dev deploys show the `[dev <user>]` prefix and paused schedules.
- [ ] Prod target has `run_as` set to a service principal, not a person.

## Checked
2026-11-01. Confirmed from the Databricks bundle pages (bundles overview, settings, deployment-modes, variables, templates): `databricks bundle init default-python`, `include`, variable `lookup`, targets `mode`, `run_as`, `root_path`, substitutions, `--var`, `BUNDLE_VAR_`, `bundle validate --output json`, development and production mode behaviours, presets precedence. Removed: other template names, the job resource example (cron, serverless environments), tests/ layout, YAML-anchor advice, `bundle generate`/`deployment bind`, `bundle summary`, and `${resources...}` substitution example.
Method: documentation only; no commands were run.
