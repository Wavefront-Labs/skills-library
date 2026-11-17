---
id: computing-software.systems-network-administration.nagios-core.event-handlers
name: event-handlers
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, event-handlers, enable-event-handlers, global-service-event-handler, event-handler-enabled, event-handler-timeout, auto-remediation, sudo]
level: practitioner
status: docs-checked
description: "Nagios Core event handlers: when they fire (SOFT/HARD problems, first recovery), enabling directives, macros to pass, run-as user and sudo, timeout."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/eventhandlers.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/configmain.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event handlers

Optional commands run on state changes, typically for auto-remediation.

## When
In a SOFT problem state, on first entering a HARD problem, and on first recovery from a SOFT or HARD problem. Global handlers run first, then the object's own. For HARD problem/recovery they run right after notifications.

## Directives
- `enable_event_handlers` (main, default 1): master switch.
- `event_handler_enabled` (object).
- `global_host_event_handler`, `global_service_event_handler` (main).
- `event_handler` (object): command name.
- `event_handler_timeout` (main): longer runs are killed and a warning logged.

## Pass state to the script
Services `$SERVICESTATE$ $SERVICESTATETYPE$ $SERVICEATTEMPT$`; hosts `$HOSTSTATE$ $HOSTSTATETYPE$ $HOSTATTEMPT$`.

## Permissions
Handlers run as the Nagios user. Restarting system services needs root, so grant only what is needed, e.g. via `sudo`.

Samples ship in `contrib/eventhandlers/` in the distribution. A worked restart example: `computing-software.systems-network-administration.nagios-core.event-handler-restart-example`.

## Checked

2026-11-04. Read the Event Handlers page as raw HTML (the stripped copy was truncated): SOFT problem, first HARD problem and first recovery triggers, global handlers before specific ones, order after notifications, the three state macros for services and hosts, contrib/eventhandlers/, nagios user permissions and sudo; main configuration page for enable_event_handlers default 1, global_host_event_handler and event_handler_timeout (killed and warning logged). Nothing removed.

Method: documentation only; no commands were run.
