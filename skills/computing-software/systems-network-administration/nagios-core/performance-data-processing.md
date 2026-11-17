---
id: computing-software.systems-network-administration.nagios-core.performance-data-processing
name: performance-data-processing
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, service-perfdata-file, service-perfdata-command, perfdata-file-template, perfdata-processing-command, perfdata-file-mode, perfdata-timeout]
level: advanced
status: docs-checked
description: "Process Nagios Core performance data with per-check commands or with spool files, templates, file mode and a periodic processing command."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/perfdata.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Processing performance data

Requires `process_performance_data` on.

## Option 1: commands
`host_perfdata_command`, `service_perfdata_command`. Most flexible but high CPU overhead; use files for many objects. Docs example writes with `/bin/echo -e` and appends a line to `/usr/local/nagios/var/service-perfdata.dat`.

## Option 2: files
| Purpose | Host | Service |
|---|---|---|
| file | `host_perfdata_file` | `service_perfdata_file` |
| line template | `..._file_template` | `..._file_template` |
| open mode | `..._file_mode` | `..._file_mode` |
| periodic command | `..._file_processing_command` | `..._file_processing_command` |
| interval | `..._file_processing_interval` | `..._file_processing_interval` |

Default mode is append; use write or non-blocking read/write for pipes. The processing command can periodically process the files, for example rotate them.

Template example:
```
service_perfdata_file_template=[SERVICEPERFDATA]\t$TIMET$\t$HOSTNAME$\t$SERVICEDESC$\t$SERVICEEXECUTIONTIME$\t$SERVICELATENCY$\t$SERVICEOUTPUT$\t$SERVICEPERFDATA$
```

`perfdata_timeout` kills slow processors and logs a warning.

Basics: `computing-software.systems-network-administration.nagios-core.performance-data-format`.

## Checked

2026-11-04. Confirmed against the Performance Data page (command and file options, template example, append default with write and non-blocking read/write, processing command and interval options, CPU overhead tip) and the main configuration page (perfdata_timeout kills commands that exceed it and logs a warning). Removed an unconfirmed grapher-loading claim.

Method: documentation only; no commands were run.
