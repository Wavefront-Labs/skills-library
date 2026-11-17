---
id: computing-software.systems-network-administration.nagios-core.state-types-soft-hard
name: state-types-soft-hard
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, state-types, soft-state, hard-state, max-check-attempts, soft-recovery, hard-recovery, servicestatetype]
level: practitioner
status: docs-checked
description: "SOFT versus HARD states in Nagios Core: when each applies, what runs in each (handlers, notifications, logging), with the max_check_attempts=3 timeline."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/statetypes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State types

State = status (OK/WARNING/UP/DOWN...) plus type (SOFT/HARD). `max_check_attempts` sets how many failed checks make a problem real.

## SOFT
Non-OK result before attempts reach max, and recovery from that. Event handlers run; NO notifications; logged only if `log_service_retries`/`log_host_retries`. `$SERVICESTATETYPE$` = SOFT.

## HARD
- Non-OK persists to max attempts.
- Hard error changes to another error state (WARNING to CRITICAL).
- Service non-OK while host is DOWN/UNREACHABLE.
- Hard recovery.
- Passive host check (unless `passive_host_checks_are_soft`).
Logged, handlers run, contacts notified.

## Timeline (max 3)
| Check | State | Type | Result |
|---|---|---|---|
| 1 | CRITICAL | SOFT | handlers |
| 2 | WARNING | SOFT | handlers |
| 3 | CRITICAL | HARD | handlers + notification, counter resets |
| after | OK | HARD | recovery notification |
| UNKNOWN then OK | | SOFT | soft recovery, no notification |

Check intervals: see `computing-software.systems-network-administration.nagios-core.active-checks`.

## Checked

2026-11-04. Confirmed on the State Types page: SOFT and HARD situations, what happens in each (logging only with log_service_retries or log_host_retries, handlers, notifications only for HARD), the SERVICESTATETYPE and HOSTSTATETYPE macros, passive host checks HARD unless passive_host_checks_are_soft, and the max_check_attempts 3 timeline including the check counter reset and soft recovery. Removed the retry_interval versus check_interval sentence, which this page does not state.

Method: documentation only; no commands were run.
