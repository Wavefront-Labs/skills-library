---
id: computing-software.data-engineering.databricks.bundle-validate-deploy-run
name: bundle-validate-deploy-run
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-asset-bundles, bundle-deploy, bundle-validate, bundle-run, bundle-destroy, databricks-cli, deployment-state, terraform]
level: practitioner
status: docs-checked
description: "Run the Databricks bundle lifecycle: validate, deploy, run, summary and destroy per target, with deployment state, locks, and recovering from drift or failed deploys."
sources:
  - https://docs.databricks.com/aws/en/dev-tools/cli/bundle-commands
  - https://docs.databricks.com/aws/en/dev-tools/bundles/work-tasks
  - https://docs.databricks.com/aws/en/dev-tools/bundles/settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bundle validate / deploy / run

**Goal:** move a bundle from laptop to workspace predictably, and recover cleanly when a deploy half-fails.

## 1. Authenticate
```bash
databricks auth login --host https://<workspace-host> --profile dev
```
Pass `--profile <profile>` to select which credentials the bundle commands use.

## 2. The lifecycle
```bash
databricks bundle validate -t dev
databricks bundle deploy   -t dev
databricks bundle run      -t dev sales_daily            # run a job or pipeline
databricks bundle run      -t dev sales_daily --params catalog=qa
databricks bundle summary  -t dev           # bundle identity, resources and deep links
databricks bundle destroy  -t dev --auto-approve         # deletes the deployed jobs, pipelines and artifacts without prompting
```
- `destroy` asks for confirmation before permanent deletion unless you pass `--auto-approve`.
- `run` on a pipeline: `--full-refresh-all` or `--refresh <table>`; on a job: `--only <task_key>[,<task_key>]` runs only those tasks.
- `bundle open sales_daily` opens the resource in the browser.

## 3. State and locks
- Prod deploys should come from CI only, so one identity owns each target's deployments.
- `databricks bundle deploy --force-lock` forces acquisition of the deployment lock and disables the guard against concurrent deployments: use it only when you are sure nobody else is deploying.
- Use the bundle `permissions:` block to restrict who can edit deployed resources.

## 4. Failure triage
| Symptom | Fix |
|---|---|
| variable has no value | give it a default or pass `--var` |
| deployment lock held | wait, or `--force-lock` after confirming no other deploy |
| artifact build fails | check the `artifacts:` build command runs locally |
| resource exists with same name | `bundle deployment bind <key> <id>` to adopt it instead of duplicating |
| deploy from wrong host | check the profile in use; set `--profile` |

## Verify
- [ ] `validate` passes in CI before `deploy`.
- [ ] `summary` URLs open the expected job in the expected workspace.
- [ ] `destroy` on a throwaway dev target removes all resources (proves nothing was created outside the bundle).

## Checked
2026-10-28. Confirmed against the Databricks CLI bundle commands page and the bundle work-tasks page (auth login --host and --profile, --params, --auto-approve on destroy and its permanent-deletion prompt, --full-refresh-all, --refresh, --only, --force-lock, bundle summary deep links, bundle open, bundle deployment bind, --var). Removed: auth describe, U2M storage note, Terraform and state-path statements, the lock-after-kill claim, UI-overwrite banner, --force branch check, BUNDLE_VAR_, specific error strings and uv build.
Method: documentation only; no commands were run.
