---
id: computing-software.data-engineering.prefect.prefect-yaml-deployments
name: prefect-yaml-deployments
category: computing-software
field: data-engineering
product: prefect
tags: [prefect-yaml, pull-steps, deploy, templating, schedules]
level: practitioner
status: docs-checked
description: "Structure of prefect.yaml, build push and pull steps, templating, schedule keys, concurrency settings and prefect deploy flags."
sources:
  - https://docs.prefect.io/v3/how-to-guides/deployments/prefect-yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: declare deployments in `prefect.yaml`.

Top-level keys: `prefect-version`, `name`, `build`, `push`, `pull`, `deployments`, optional `definitions` for YAML anchors (`&name`, `*name`, `<<:`).

Deployment keys: `name` (unique per file), `version`, `tags`, `description`, `schedules`, `concurrency_limit`, `triggers`, `entrypoint` (`file.py:flow_fn` or module path), `parameters`, `enforce_parameter_schema`, `work_pool` (`name`, `work_queue_name`, `job_variables`), and per-deployment `build`, `push`, `pull` that override the top level.

Steps run in order, each keyed by an importable function path (optional `id`, `requires`). `pull` is the only required action. Omitted or `null` `pull` generates `set_working_directory`; use `pull: []` to disable. Common pull steps: `set_working_directory`, `git_clone`, `pull_from_<cloud>`, `pip_install_requirements`, `run_shell_script` (`script`, `stream_output`, `expand_env_vars`, `shell`).

Templating: `{{ step-id.field }}`, `{{ prefect.blocks.<type>.<slug> }}`, `{{ prefect.variables.<name> }}`, `{{ $ENV_VAR }}`. Block and variable references in `pull` resolve at runtime.

Schedules: `interval`, `anchor_date`, `timezone`, `cron`, `day_or`, `rrule`; `interval` cannot combine with `cron` or `rrule`. `schedules: []` preserves existing schedules unless `PREFECT_DEPLOYMENTS_CLEAR_SCHEDULES_ON_EMPTY=true`.

Concurrency: an integer, or `limit`, `collision_strategy` (`ENQUEUE` default, `CANCEL_NEW`), `grace_period_seconds` (60 to 86400).

CLI: `prefect init [--recipe NAME] [--field key=value]`; `prefect deploy` with `--name/-n` (repeatable, wildcards), `--all`, `--prefect-file PATH`; `prefect --no-prompt deploy` for CI.

## Checked

2026-11-09. Read the whole prefect.yaml page. Confirmed the top-level and deployment keys, step format, omitted versus empty pull, templating forms, schedule and concurrency fields, and the deploy and init flags. Removed nothing.

Method: documentation only; no commands were run.
