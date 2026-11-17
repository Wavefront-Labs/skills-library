---
id: computing-software.systems-network-administration.icinga-2.host-and-service-states-and-hard-soft
name: host-and-service-states-and-hard-soft
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, host-states, service-states, hard-state, soft-state, max-check-attempts, retry-interval, exit-codes]
level: intro
status: docs-checked
description: Icinga 2 host and service states, plugin exit code mapping, and how max_check_attempts, check_interval and retry_interval drive SOFT versus HARD states before notifications.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# host and service states, hard and soft
Hosts are UP or DOWN. Services are OK, WARNING, CRITICAL or UNKNOWN (UNKNOWN: the check could not determine the state). Runtime macros also expose host state `UNREACHABLE`.

Plugin exit code mapping:

| Value | Host | Service |
|---|---|---|
| 0 | Up | OK |
| 1 | Up | Warning |
| 2 | Down | Critical |
| 3 | Down | Unknown |

Services map states directly while hosts treat 0 or 1 as UP.

**SOFT vs HARD.** On detecting a problem Icinga re-checks the object `max_check_attempts` times using `retry_interval`. During this time the object is in a SOFT state, which avoids notifications for transient failures. When re-checks are exhausted and the state is still non-OK, it becomes HARD and notifications are sent. In HARD state `check_interval` applies.

Example template using these attributes:
```
template Service "generic-service" {
  max_check_attempts = 3
  check_interval = 5m
  retry_interval = 1m
  enable_perfdata = true
}
```
Runtime macros `service.state_type`, `service.check_attempt` and `service.max_check_attempts` expose the current values.

## Checked

2026-11-04. Confirmed against the Icinga 2 monitoring basics chapter: host and service states including UNREACHABLE, exit code mapping, SOFT and HARD state attempts and intervals.

Method: documentation only; no commands were run.
