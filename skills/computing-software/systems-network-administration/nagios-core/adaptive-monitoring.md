---
id: computing-software.systems-network-administration.nagios-core.adaptive-monitoring
name: adaptive-monitoring
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, adaptive-monitoring, runtime-changes, external-commands, change-check-command, change-event-handler, command-file]
level: advanced
status: docs-checked
description: "Adaptive monitoring in Nagios Core: which host, service and global attributes can be changed at runtime through external commands, and the predefined command constraint."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/adaptive.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Adaptive monitoring

Change monitoring behaviour while Nagios runs, by submitting external commands to the file named in `command_file`.

## Changeable at runtime
- **Services and hosts:** check command (and arguments), check interval, max check attempts, check timeperiod, event handler command (and arguments).
- **Global:** the global host and service event handler commands (and arguments).

## Constraint
Commands, timeperiods and event handlers referenced in a change MUST already be defined when Nagios started; requests naming undefined ones are ignored.

## Arguments
Command arguments are appended to the command name separated by `!`.

## Notes
- The page does not list the command names; use the Nagios Core External Commands reference.

Mechanics: `computing-software.systems-network-administration.nagios-core.external-commands`.

## Checked

2026-11-04. Confirmed against the Adaptive Monitoring page: changeable service, host and global attributes, the requirement that new commands and timeperiods were defined before Nagios started, and the bang-separated arguments. Page lists commands only via an external link.

Method: documentation only; no commands were run.
