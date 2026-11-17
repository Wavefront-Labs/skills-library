---
id: computing-software.data-engineering.dagster.troubleshooting-schedules
name: troubleshooting-schedules
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, troubleshooting, schedule-not-running, daemon, scheduler, reload-definitions]
level: practitioner
status: docs-checked
description: "Diagnose a Dagster schedule that does not fire: started toggle, failed ticks, next tick, stale code, scheduler daemon and workspace.yaml."
sources:
  - https://docs.dagster.io/guides/automate/schedules/troubleshooting-schedules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting schedules

The docs give five steps, in this order.
1. Started? **Automation** in the top nav; started schedules have an enabled toggle in the **Running** column.
2. Failures? **Last tick** column; a **Failed** badge opens the error and stack trace.
3. Interval? The **Schedule** column shows **Next tick**; verify the time, including the timezone.
4. Latest code? Local webserver or OSS: **Settings > Code locations > Reload definitions**. Dagster+: **Deployment > Code locations**, find the location, **Redeploy**. A code location that cannot load (for example a syntax error) has Status **Failed** with a **View error** link.
5. OSS only, dagster-daemon: **Deployment > Daemons**, **Scheduler** row. The daemon sends periodic heartbeats; status **Not running** indicates a daemon deployment problem, and errors often show on that tab. Then check the daemon process logs (on Kubernetes, the pod running the daemon) and search for the schedule name or `SchedulerDaemon`.

Gotcha: if daemon logs say the schedule could not be found, verify the daemon uses the same `workspace.yaml` as the webserver. The daemon does not need to restart to pick up `workspace.yaml` changes.

## Checked
2026-11-08. Confirmed against the Dagster docs page Troubleshooting schedules (raw markdown from the docs repo): all five steps, Dagster+ versus OSS paths, workspace.yaml note. Minor wording tightening; nothing removed.
Method: documentation only; no commands were run.
