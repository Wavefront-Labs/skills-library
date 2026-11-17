---
id: computing-software.systems-network-administration.nagios-core.freshness-checking
name: freshness-checking
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, freshness, freshness-checking, check-freshness, freshness-threshold, stale-results, passive-checks, check-dummy]
level: practitioner
status: docs-checked
description: "Detect missing passive results in Nagios Core with freshness checking: global switches, check_freshness, freshness_threshold and a stale-result active check command."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/freshness.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/configmain.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Freshness checking

If an object's latest result is older than its threshold, Nagios marks it stale and runs its `check_command` as an active check, even if active checks are disabled.

## Directives
- Main: `check_service_freshness`, `check_host_freshness`, `service_freshness_check_interval`, `host_freshness_check_interval`, `additional_freshness_latency` (seconds added to auto thresholds).
- Object: `check_freshness 1`, `freshness_threshold` (seconds; omitted/0 = auto-calculated, but set it explicitly), `check_command`, `check_period` (must be valid).

## Example (nightly backup report)
`active_checks_enabled 0`, `passive_checks_enabled 1`, `check_freshness 1`, `freshness_threshold 93600` (26 hours allowing for late jobs). If no report arrives, `check_command no-backup-report` runs `check_dummy` with a critical result, so the service goes CRITICAL and notifies.

## Why
Passive results silently stop when the sender dies; freshness converts silence into an alert.

Related: `computing-software.systems-network-administration.nagios-core.passive-checks`.

## Checked

2026-11-04. Confirmed on the Freshness Checking page (stale result forces an active check even if active checks are disabled, the five enabling steps, auto-calculated threshold and the advice to set one explicitly, backup report example with 93600 seconds and check_dummy) and the main configuration page (check_service_freshness, check_host_freshness, the two interval options in seconds, additional_freshness_latency). Nothing removed.

Method: documentation only; no commands were run.
