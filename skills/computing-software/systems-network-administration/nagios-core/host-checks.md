---
id: computing-software.systems-network-administration.nagios-core.host-checks
name: host-checks
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, host-checks, scheduled-checks, on-demand-checks, check-interval, host-check-parallelization, max-check-attempts]
level: practitioner
status: docs-checked
description: "When Nagios Core runs host checks (scheduled and on-demand), how results map to UP/DOWN/UNREACHABLE, parallelism, and the max_check_attempts 1 pitfall."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/hostchecks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Host checks

## When they run
- Scheduled at `check_interval` / `retry_interval`. `check_interval 0` disables scheduled checks but on-demand ones still run.
- On demand when a service on the host changes state, for reachability logic, and for predictive dependency checks.

## State mapping
OK -> UP; WARNING -> UP (DOWN with `use_aggressive_host_checking`); UNKNOWN and CRITICAL -> DOWN. A preliminary DOWN is checked against `parents`: if at least one parent is UP the host stays DOWN; if all parents are DOWN/UNREACHABLE it becomes UNREACHABLE.

## Execution
Checks run in forked children and report to the daemon, which then runs event handlers and notifications. Secondary checks are normally parallel, except that hosts with `max_check_attempts 1` have their immediate parents checked serially, which can seriously hurt performance. Use a value above 1.

## Related
Cached results can replace on-demand checks (`computing-software.systems-network-administration.nagios-core.cached-checks`). Execution dependencies can block checks.

## Checked

2026-11-04. Confirmed against the Host Checks page: scheduling and on-demand triggers, check_interval 0 behaviour, state mapping tables including use_aggressive_host_checking and parents, forked parallel execution, and the max_check_attempts 1 serial parent check problem. Removed an unconfirmed web UI self-check.

Method: documentation only; no commands were run.
