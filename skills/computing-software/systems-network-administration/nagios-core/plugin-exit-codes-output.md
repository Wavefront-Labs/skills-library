---
id: computing-software.systems-network-administration.nagios-core.plugin-exit-codes-output
name: plugin-exit-codes-output
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, plugin-api, plugin-exit-codes, plugin-output, longserviceoutput, multi-line-output, perfdata-separator, max-plugin-output-length]
level: practitioner
status: docs-checked
description: "Nagios plugin contract: exit codes 0-3 and their host/service meaning, one-line text plus optional pipe-separated perfdata, multi-line output macros, 4 KB limit."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/pluginapi.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plugin return codes and output

| Exit | Service | Host |
|---|---|---|
| 0 | OK | UP |
| 1 | WARNING | UP (DOWN/UNREACHABLE if `use_aggressive_host_checking`) |
| 2 | CRITICAL | DOWN/UNREACHABLE |
| 3 | UNKNOWN | DOWN/UNREACHABLE |

## Output
- At least one line of text to STDOUT.
- Performance data follows a `|`; it may be on the first line, later lines, both or neither.
- Multi-line output (Core 3+):
  - `$SERVICEOUTPUT$` = first line, left of pipe
  - `$SERVICEPERFDATA$` = perfdata from all lines, space-joined
  - `$LONGSERVICEOUTPUT$` = remaining lines, joined with escaped newlines
- Example perfdata item: `/=2643MB;5948;5958;0;5968`.
- Only the first 4 KB of output is read. To raise it, change `MAX_PLUGIN_OUTPUT_LENGTH` in `include/nagios.h.in` and recompile.

## Writing plugins
The page defers to the Nagios Plugins development guidelines and says to study official plugin source (C, Perl, shell).

## Self-check
`./check_x; echo $?` returns 0-3 and prints one status line.

## Checked

2026-11-04. Confirmed on the Plugin API page: return code table with host states and the use_aggressive_host_checking note, one text line to STDOUT minimum, pipe-separated perfdata in first and later lines or neither, SERVICEOUTPUT, SERVICEPERFDATA (space-joined) and LONGSERVICEOUTPUT (escaped newlines) values from the page's worked example, 4 KB read limit and MAX_PLUGIN_OUTPUT_LENGTH in include/nagios.h.in with recompile, and the pointer to official plugins and development guidelines. Nothing removed.

Method: documentation only; no commands were run.
