---
id: computing-software.systems-network-administration.healthchecks.check-states
name: check-states
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, check-states, dead-mans-switch, late-status, paused-status]
level: intro
status: docs-checked
description: "What Healthchecks monitors and its check states: new, up, late, down and paused, plus the started indicator, a dead man's switch model and unsuitable uses."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/introduction.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Healthchecks is a dead man's switch for cron jobs and other periodic processes: jobs send HTTP pings, and an alert fires when an expected ping is missed. It suits backups, task queues, replication monitoring, report generation, data sync, antivirus scans, DDNS updaters and SSL renewal scripts.

It is not for probing website uptime, collecting application metrics or log aggregation.

One check represents one monitored service (for cron, one check per job). Each has a ping URL, a schedule and assigned integrations.

States:
- New: created, no pings yet.
- Up: the latest success signal arrived on time.
- Late: a success is due but missing; still inside grace time.
- Down: success missing and grace time elapsed; alerts go out.
- Paused: monitoring manually suspended, for example for a known unresolved issue.
- Started: three animated dots under the status icon when the latest signal is a start.

Check UUIDs and project ping keys are secrets; anyone holding them can send signals.

Projects group checks and integrations. Each has its own name, API keys and team; checks can move between projects keeping their ping URLs.

## Checked

2026-11-04: confirmed against the introduction page (dead man's switch, use cases and non-uses, five states plus started indicator, secrets, projects).
Method: documentation only; no commands were run.
