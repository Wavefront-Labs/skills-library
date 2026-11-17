---
id: computing-software.systems-network-administration.icinga-2.api-actions-check-results-downtimes-acks
name: api-actions-check-results-downtimes-acks
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, rest-api, actions, process-check-result, schedule-downtime, acknowledge-problem, reschedule-check]
level: practitioner
status: docs-checked
description: Drive Icinga 2 through POST /v1/actions - process-check-result, reschedule-check, acknowledge-problem, schedule-downtime, notifications, generate-ticket, execute-command.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API actions
Send `POST` to `/v1/actions/<action>`; each matching object returns its own status. Most actions need a `type` (`Host` or `Service`) and a `filter`. Timestamps are Unix seconds. Program-wide switches (such as notifications) are changed on the IcingaApplication object `app` via `attrs` (`enable_notifications`).

- **process-check-result:** `exit_status` (services 0=OK, 1=WARNING, 2=CRITICAL, 3=UNKNOWN; hosts 0=UP, 1=DOWN) and `plugin_output` required. Optional `performance_data` (array), `check_command`, `check_source`, `execution_start`, `execution_end`, `ttl` (the next expected result is now plus ttl, used by freshness checks). Multi-line output: first line is short output, the rest long output.
- **reschedule-check:** `next_check` (default now), `force` (ignore time periods and disabled checks).
- **send-custom-notification:** `author`, `comment`, optional `force`.
- **delay-notification:** `timestamp`.
- **acknowledge-problem:** `author` and `comment` required; optional `expiry`, `sticky`, `notify`, `persistent`, `set_time`. Counterpart: `remove-acknowledgement`.
- **schedule-downtime:** `author`, `comment`, `start_time`, `end_time` required; `fixed` defaults to true; flexible downtimes need `duration`. Options: `all_services`, `trigger_name`, `child_options`. Remove with `remove-downtime`.
- **add-comment / remove-comment**, **generate-ticket** (`cn`, for CSR auto-signing), **shutdown-process** and **restart-process** (no type or filter), **execute-command** (`ttl` required).

Permissions needed: `actions/<action>`.

## Checked

2026-11-04. Confirmed against the Icinga 2 API chapter: action parameters for process-check-result, reschedule-check, schedule-downtime (fixed defaults to true), ttl and execute-command.

Method: documentation only; no commands were run.
