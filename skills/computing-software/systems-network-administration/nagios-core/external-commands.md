---
id: computing-software.systems-network-administration.nagios-core.external-commands
name: external-commands
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, external-commands, command-file, check-external-commands, nagios-cmd, command-format, command-file-permissions]
level: practitioner
status: docs-checked
description: "Control a running Nagios Core through the external command file: check_external_commands, command_file, the [time] COMMAND;args format, FIFO behaviour and permissions."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/extcommands.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/configmain.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External commands

External apps (including the CGIs) change behaviour at runtime: disable notifications or checks, force a check, add comments, submit passive results.

## Enable
- `check_external_commands=1` (default 1).
- `command_file=<path>`: a named pipe (FIFO) created at start, removed at shutdown; Nagios exits with an error if it already exists at start.
- Directory permissions: only the nagios user and the web server user should write to the command file directory (`/usr/local/nagios/var/rw`).

## Format
```
[<time_t>] COMMAND_ID;arguments
```
`time` is when the application submitted it. Command IDs and arguments are in the separate External Commands reference (nagios.org, "Nagios Core External Commands").

## Processing
Since Core 4 commands are processed as soon as received; the deprecated `command_check_interval` and `external_command_buffer_slots` have no effect.

## Logging
`log_external_commands` (default 1).

## Used by
Passive checks, downtime scripting, adaptive monitoring:
`computing-software.systems-network-administration.nagios-core.passive-check-submission`, `computing-software.systems-network-administration.nagios-core.adaptive-monitoring`.

## Checked

2026-11-04. Confirmed on the External Commands page (check_external_commands, command_file, permissions on the command file directory, [time] command_id;arguments in time_t, processed as soon as received since Core 4), the main configuration page (command_file is a FIFO created at start and removed at shutdown, Nagios terminates if it already exists, command_check_interval and external_command_buffer_slots deprecated with no effect) and the security page (only the nagios and web server users may write in var/rw). Nothing removed.

Method: documentation only; no commands were run.
