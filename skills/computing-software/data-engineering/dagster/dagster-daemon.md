---
id: computing-software.data-engineering.dagster.dagster-daemon
name: dagster-daemon
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, dagster-daemon, scheduler-daemon, sensor-daemon, run-queue-daemon, dagster-dev]
level: practitioner
status: docs-checked
description: "Run and check the Dagster daemon (dagster dev or dagster-daemon run), know which sub-daemons exist and how to read the Daemons tab."
sources:
  - https://docs.dagster.io/deployment/execution/dagster-daemon
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dagster daemon

Schedules, sensors and run queueing need a long-running `dagster-daemon` process in your deployment.

## Start
- Local full stack: `dagster dev` (launches webserver and daemon).
- Daemon only: `dagster-daemon run` (takes the same arguments as `dagster dev` for locating your code).
- Docker or Kubernetes: see the deployment options documentation.

## Daemons (included based on the instance file; each runs on a regular interval in its own threads)
- Scheduler daemon: creates runs from active schedules; enabled as long as the default `DagsterDaemonScheduler` is not overridden as the instance scheduler.
- Run queue daemon: launches queued runs, taking into account limits and prioritization rules; enabled by setting `QueuedRunCoordinator` as the run coordinator.
- Sensor daemon: creates runs from active sensors that are turned on; always enabled.
- Run monitoring daemon: handles run worker failures; enabled by the `run_monitoring` field in the instance.

If the daemon uses a workspace file to load code locations, it periodically reloads the file, so it does not need restarting when workspace files change.

## Status
UI: **Deployment** then the **Daemons** tab shows all daemons configured on the instance. Each daemon periodically writes a heartbeat to instance storage; if one has no recent heartbeat, check the logs of the `dagster-daemon` process for errors.

## Checked
2026-11-08. Confirmed against the Dagster docs page Dagster daemon (raw markdown from the docs repo): start commands, the four-daemon table, workspace reload, Daemons tab and heartbeat note. Nothing removed.
Method: documentation only; no commands were run.
