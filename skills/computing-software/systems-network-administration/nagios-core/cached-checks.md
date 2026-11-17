---
id: computing-software.systems-network-administration.nagios-core.cached-checks
name: cached-checks
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, cached-checks, cached-host-check-horizon, cached-service-check-horizon, on-demand-checks, check-latency, tuning]
level: advanced
status: docs-checked
description: "Cached checks in Nagios Core: reuse a recent result for on-demand checks via cached_host_check_horizon and cached_service_check_horizon, the staleness trade-off and tuning steps."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/cachedchecks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cached checks

Skip running a plugin for an ON-DEMAND check when the last result is recent enough. Scheduled checks gain nothing.

- On-demand host checks: a service on the host changes state, reachability logic, predictive dependency checks.
- On-demand service checks: only predictive service dependency checks, so host caching gives most of the gain.

## Config
`cached_host_check_horizon`, `cached_service_check_horizon` (seconds; docs example 15; 0 disables).

## Trade-off
Longer horizon = faster, but stale state can cause false notifications. Setting it equal to a host's check interval could in theory give 100% hit rate. Some sites disable caching for reliability.

## Tuning steps
1. Schedule regular host checks (`check_interval` > 0) and `max_check_attempts` > 1.
2. Graph `nagiostats` output with MRTG to compare on-demand plugin runs vs cache hits.
3. Adjust horizons, keep watching.

Docs example: 44 hosts, 5-minute interval, 15 s horizon: about 9 of 53 checks on-demand (17%), roughly 22% of those served from cache.

See `computing-software.systems-network-administration.nagios-core.nagiostats-mrtg`.

## Checked

2026-11-04. Confirmed against the Cached Checks page (on-demand only, horizons, trade-off, tuning steps, 44 hosts / 5-minute / 15 s example with 9 of 53 and 2 of 9) and the main configuration page (cached_host_check_horizon and cached_service_check_horizon in seconds, example 15, 0 disables).

Method: documentation only; no commands were run.
