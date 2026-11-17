---
id: computing-software.systems-network-administration.nagios-core.state-stalking
name: state-stalking
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, stalking, stalking-options, state-stalking, log-output-changes, notification-stalking, alert-histogram]
level: advanced
status: docs-checked
description: "Use Nagios Core stalking_options to log a check when its output changes within the same state; the N option (4.4.0+), examples, and effect on alert reports."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/stalking.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State stalking

Logs a result whenever its output differs from the previous check, even if the state is unchanged. Purely for logging; volatile services additionally notify and run handlers.

## Enable
`stalking_options` in a host or service. Pick states: host `o,d,u`; service `o,w,u,c`. Stalk WARNING and CRITICAL only, for example, to leave OK/UNKNOWN unlogged.

**`N`** (Core 4.4.0+): log the state each time a notification is sent (hourly renotify gives one line per hour).

## Examples
- RAID service with CRITICAL stalking: normal logging records only OK to WARNING and WARNING to CRITICAL; stalking also records each change in the CRITICAL text (drive count details, then "array failed").
- `check_http` WARNING for a 404, later WARNING for a missing text pattern: stalking WARNING records the change of cause.

## Use when
You need archived evolution of a problem, the plugin varies its text within one state, and only some objects/states need it.

## Avoid when
Output is constant per state, or you have no clear need. Extra entries inflate counts in the histogram and alert summary CGIs.

## Checked

2026-11-04. Confirmed against the State Stalking page (log on output change, RAID and check_http examples, stalking_options, volatile services differ by notifying and running handlers, N option from Core 4.4.0, report inflation caveat) and the Object Definitions page (host o,d,u and service o,w,u,c stalking letters).

Method: documentation only; no commands were run.
