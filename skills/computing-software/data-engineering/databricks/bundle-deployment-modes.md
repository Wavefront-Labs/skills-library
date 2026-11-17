---
id: computing-software.data-engineering.databricks.bundle-deployment-modes
name: bundle-deployment-modes
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-asset-bundles, bundle-deployment-modes, mode-development, mode-production, presets, run-as, targets]
level: practitioner
status: docs-checked
description: "Configure Databricks Asset Bundle targets with mode development vs production: name prefixes, paused schedules, run_as and permissions checks, presets, and per-target overrides."
sources:
  - https://docs.databricks.com/en/dev-tools/bundles/deployment-modes.html
  - https://docs.databricks.com/en/dev-tools/bundles/settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bundle deployment modes

**Goal:** every developer deploys an isolated copy of the jobs/pipelines, while production deploys are locked down and deterministic.

## Targets
```yaml
bundle:
  name: sales_etl

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
    run_as:
      service_principal_name: <SERVICE_PRINCIPAL_APP_ID>
    # also set `permissions` explicitly; production mode validates run_as and permissions
```

## What `mode: development` does
- Prefixes resources that are not files or notebooks with `[dev ${workspace.current_user.short_name}]` and tags each deployed job and pipeline with a `dev` tag.
- **Pauses** all schedules and triggers on deployed resources; set `pause_status` to `UNPAUSED` on an individual job to run it.
- Marks deployed pipelines `development: true`.
- Enables concurrent runs on all deployed jobs; set `max_concurrent_runs` to 1 to disable for one job.
- Enables `--cluster-id` on `bundle deploy` to override existing cluster definitions.
- Disables the deployment lock for faster iteration (re-enable with `bundle.deployment.lock.enabled: true`).

## What `mode: production` does
- Validates that deployed pipelines are `development: false`.
- Validates that the current Git branch equals the target's `git.branch` when one is configured; `--force` overrides this.
- Databricks recommends a service principal via `run_as`. Without one, it validates that `artifact_path`, `file_path`, `root_path` and `state_path` are not overridden to a specific user, and that `run_as` and `permissions` are specified.
- Does not allow overriding cluster definitions (for example with `--compute-id`).

## Presets (custom behaviours)
```yaml
targets:
  staging:
    presets:
      name_prefix: "[staging] "
      trigger_pause_status: PAUSED
      jobs_max_concurrent_runs: 1
      tags: {env: staging}
      pipelines_development: true
```
Presets let you mix behaviours without full development mode. If both `mode` and `presets` are set, presets override the mode defaults, and settings on individual resources override presets.

## Per-target overrides
```yaml
targets:
  prod:
    resources:
      jobs:
        sales_daily:
          job_clusters:
            - job_cluster_key: main
              new_cluster: {num_workers: 8}
    variables:
      catalog: prod
```

## Gotchas
- Development-mode resources persist after you stop working; `databricks bundle destroy -t dev` cleans them up.
- The development prefix is part of the resource name, so use separate dev and prod targets rather than switching one target's mode.

## Verify
- [ ] `databricks bundle validate -t prod` passes with no warnings about permissions/run_as.
- [ ] Dev deploy shows `[dev <short_name>]` jobs with paused schedules.

## Checked
2026-10-28 Confirmed on the Databricks bundle deployment modes page: development-mode behaviours (prefix, dev tag, paused schedules and triggers, pipelines development: true, concurrent runs, `--cluster-id`, deployment lock), production-mode validations (pipelines, git branch and `--force`, `run_as` and `permissions`, path overrides, no cluster override), and the presets `name_prefix`, `trigger_pause_status`, `jobs_max_concurrent_runs`, `tags`, `pipelines_development` plus precedence. Removed or corrected: `--compute-id` in development mode (the page says `--cluster-id`), the home-folder deploy path, the pipeline retry note, the root_path and no-prefix claims, the `CAN_VIEW`/`CAN_MANAGE` permission levels, the mode-switch and pipeline run_as claims, and the sample workspace host and service principal IDs.
Method: documentation only; no commands were run.
