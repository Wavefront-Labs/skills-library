---
id: computing-software.systems-network-administration.nagios-core.volatile-services
name: volatile-services
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, volatile-services, is-volatile, snmp-traps, security-alerts, portsentry, passive-checks, event-driven-alerts]
level: advanced
status: docs-checked
description: "Volatile services in Nagios Core: is_volatile makes every non-OK result log, notify and run handlers; pair with passive checks for traps and alerts, PortSentry example."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/volatileservices.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Volatile services

`is_volatile 1` in a service definition. Use for services that reset themselves to OK on each check, or events (security alerts) needing attention every time.

## Behaviour difference
When a volatile service is in a hard non-OK state and another non-OK result arrives (no state change), Nagios:
- logs it each time,
- notifies contacts each time (notification intervals are ignored),
- runs the event handler.
A normal service does this only on first entering the hard non-OK state.

If you only need logging, use stalking instead (`computing-software.systems-network-administration.nagios-core.state-stalking`).

## Example: PortSentry port-scan alert
Service settings: `max_check_attempts 1` (immediate HARD), `active_checks_enabled 0`, `passive_checks_enabled 1`, `is_volatile 1`. PortSentry's `KILL_RUN_CMD` runs a `submit_check_result` script that writes a `PROCESS_SERVICE_CHECK_RESULT` with return code 2. Each scan repeats logging, notification and handler.

Submission format: `computing-software.systems-network-administration.nagios-core.passive-check-submission`.

## Checked

2026-11-04. Confirmed against the Volatile Services page: is_volatile behaviour (logged, notified with intervals ignored, event handler run), stalking tip, and the PortSentry example settings (max_check_attempts 1, active checks off, passive on, is_volatile 1, KILL_RUN_CMD, PROCESS_SERVICE_CHECK_RESULT with return code 2).

Method: documentation only; no commands were run.
