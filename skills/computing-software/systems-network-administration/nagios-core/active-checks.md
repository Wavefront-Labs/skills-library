---
id: computing-software.systems-network-administration.nagios-core.active-checks
name: active-checks
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, active-checks, check-interval, retry-interval, on-demand-checks, execute-service-checks, execute-host-checks]
level: intro
status: docs-checked
description: "Active checks in Nagios Core are initiated by the daemon itself: scheduled at check_interval (HARD) or retry_interval (SOFT), plus on-demand reachability and dependency checks."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/activechecks.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/configmain.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active checks

The daemon starts each check: it runs a plugin against the host or service, receives the result, then acts (notifications, event handlers).

## Scheduling
- `check_interval`: used while the object is in a HARD state.
- `retry_interval`: used while in a SOFT state.
- Checks only run inside `check_period`.

## On-demand triggers
- Reachability: checking parent and child hosts to assess a network segment.
- Predictive dependency checks.

## Switches
- Global: `execute_service_checks`, `execute_host_checks` (default 1).
- Per object: `active_checks_enabled` (default 1).
- Initial spread at startup: `service_inter_check_delay_method` (default `s`), `max_service_check_spread` (30 minutes).
- Parallel cap: `max_concurrent_checks` (0 = unlimited).

Compare with externally-started results: `computing-software.systems-network-administration.nagios-core.passive-checks`.

Self-check: with `execute_service_checks=0` the daemon does not run service checks (it can still accept passive results).

## Checked

2026-11-04. Confirmed against the Active Checks page (check_interval for HARD, retry_interval for SOFT, on-demand reachability and predictive dependency checks) and the main configuration page (execute_service_checks and execute_host_checks default 1, service_inter_check_delay_method default s, max_service_check_spread default 30 minutes, max_concurrent_checks 0 default unrestricted). Replaced the unconfirmed web UI self-check with the documented behaviour of disabling service checks.

Method: documentation only; no commands were run.
