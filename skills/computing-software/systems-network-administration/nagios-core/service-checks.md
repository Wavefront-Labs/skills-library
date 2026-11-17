---
id: computing-software.systems-network-administration.nagios-core.service-checks
name: service-checks
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, service-checks, scheduled-checks, service-states, check-execution, forked-child, service-dependencies-on-demand]
level: practitioner
status: docs-checked
description: "How Nagios Core runs service checks: scheduled at check_interval/retry_interval, on-demand only for dependencies, parallel forked children, four service states."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/servicechecks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service checks

## When
- **Scheduled** by `check_interval` and `retry_interval` in the service definition.
- **On demand** only for predictive service dependency checks. Without service dependencies there are no on-demand service checks, so cached checks barely help services.

## Execution model
Each check runs in a child process forked from the daemon; scheduled and on-demand checks run in parallel. The child reports to the parent, which processes the result, then runs event handlers and sends notifications.

## States
OK, WARNING, UNKNOWN, CRITICAL map directly from plugin results (`computing-software.systems-network-administration.nagios-core.plugin-exit-codes-output`).

## Consequences of a state change
Tracked as HARD or SOFT (`computing-software.systems-network-administration.nagios-core.state-types-soft-hard`); may trigger handlers, notifications and on-demand host checks. Services that change too often are marked flapping and notifications are suppressed until stable.

## Limits
`service_check_timeout` caps run time; a timed-out check returns the state in `service_check_timeout_state` (default CRITICAL).

## Checked

2026-11-04. Confirmed against the Service Checks page (check_interval and retry_interval, on-demand only for predictive dependency checks, cached checks only help with dependencies, forked parallel children, four states mapped directly, HARD or SOFT, flapping) and the main configuration page (service_check_timeout kills checks, service_check_timeout_state default CRITICAL). Removed an unconfirmed self-check.

Method: documentation only; no commands were run.
