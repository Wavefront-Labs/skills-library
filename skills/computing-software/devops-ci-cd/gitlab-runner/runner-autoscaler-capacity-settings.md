---
id: computing-software.devops-ci-cd.gitlab-runner.runner-autoscaler-capacity-settings
name: runner-autoscaler-capacity-settings
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [autoscaler, capacity-per-instance, max-use-count, max-instances, instance-ready-command]
level: advanced
status: docs-checked
description: "Core [runners.autoscaler] settings that bound instances and jobs per instance."
sources: ["https://docs.gitlab.com/runner/configuration/advanced-configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Autoscaler capacity settings

Under `[runners.autoscaler]`:
- `plugin`: fleeting plugin to use.
- `capacity_per_instance`: jobs one instance runs at once.
- `max_use_count`: jobs before an instance is retired.
- `max_instances`: maximum instances allowed regardless of state (pending, running, deleting); default `0` (unlimited).
- `instance_ready_command`: command run on each provisioned instance to ensure it is ready; a failure removes the instance (16.11).
- `instance_acquire_timeout`: how long a job waits for an instance; default `15m` (18.1).
- `update_interval`: how often instance state is refreshed; default `1m`.
- `failure_threshold`: consecutive health failures before the fleeting plugin replaces an instance; default `3` (18.4).
- `[runners.autoscaler.scale_throttle]`: `limit` is new instances per second (`-1` infinite, default `0` means 100) and `burst` the quota size.

## Checked

2026-11-03. Confirmed against autoscaler settings and scale_throttle on Advanced configuration. Removed: the unsourced capacity formula; corrected max_instances (default 0, unlimited) and failure_threshold wording.

Method: documentation only; no commands were run.
