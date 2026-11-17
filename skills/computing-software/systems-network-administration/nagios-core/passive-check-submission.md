---
id: computing-software.systems-network-administration.nagios-core.passive-check-submission
name: passive-check-submission
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, process-service-check-result, process-host-check-result, external-command-format, return-code, command-file, passive-checks]
level: practitioner
status: docs-checked
description: "Exact PROCESS_SERVICE_CHECK_RESULT and PROCESS_HOST_CHECK_RESULT command lines to write into the Nagios Core command file, with return codes and timestamp rules."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/passivechecks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Submitting passive results

## Service
```
[<timestamp>] PROCESS_SERVICE_CHECK_RESULT;<host_name>;<svc_description>;<return_code>;<plugin_output>
```
- `timestamp`: time_t (seconds since epoch), then ONE space after the bracket.
- `host_name`: short name from the host definition.
- `svc_description`: must match the service definition.
- `return_code`: 0 OK, 1 WARNING, 2 CRITICAL, 3 UNKNOWN.

## Host
```
[<timestamp>] PROCESS_HOST_CHECK_RESULT;<host_name>;<host_status>;<plugin_output>
```
`host_status`: 0 UP, 1 DOWN, 2 UNREACHABLE.

## Example write
```
now=$(date +%s)
echo "[$now] PROCESS_SERVICE_CHECK_RESULT;web01;Backup;0;OK - done" >> /usr/local/nagios/var/rw/nagios.cmd
```
(command file path is whatever `command_file` says; the directory must be writable by the submitting user.)

## Gotchas
- Definitions must exist as of the last restart, or results are ignored.
- Passive host results are taken as truth with no reachability logic unless `translate_passive_host_checks` is on.

Concepts: `computing-software.systems-network-administration.nagios-core.passive-checks`.

## Checked

2026-11-04. Confirmed on the Passive Checks page: both command formats, time_t timestamp with a single space after the bracket, return codes 0 to 3, host status 0 to 2, the rule that objects must exist at the last restart, and the translate_passive_host_checks note; the example write now follows the append-to-command-file script on the Volatile Services page.

Method: documentation only; no commands were run.
