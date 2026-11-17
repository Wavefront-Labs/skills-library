---
id: computing-software.systems-network-administration.windows-server.data-collector-sets-and-logman
name: data-collector-sets-and-logman
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, performance-monitoring, perfmon, data-collector-sets, logman, relog, performance-baseline, blg]
level: practitioner
status: docs-checked
description: "Capture performance baselines with Data Collector Sets and logman: counter collectors, sample intervals, circular logs, schedules, export/import and relog conversion."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/logman
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/logman-create-counter
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/logman-import-export
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/relog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data collector sets and logman

## Create a baseline collector
```
logman create counter Baseline -c "\Processor(_Total)\% Processor time" <more counter paths> ^
  -si 00:00:15 -f bincirc -max 1024 -o "<LOG_FOLDER>\Baseline" -v mmddhhmm
logman start Baseline
logman query Baseline
```
- `-c` takes one or more counter paths; for a long list use `-cf <file>` (one counter path per line).
- `-si [[hh:]mm:]ss` is the sample interval; `-sc` caps the number of samples; `-rf` runs for a set period.
- `-f` is the log format: `bin`, `bincirc`, `csv`, `tsv` or `sql` (csv logs are limited to 2 GB). `-max` is the maximum log size in MB, so `-f bincirc -max 1024` is a circular binary log capped at 1024 MB.
- `-v nnnnnn|mmddhhmm` appends versioning information to the log file name; `-cnf` starts a new file after a time or when the maximum size is exceeded.
- Remote: add `-s <computer name>`; this works for `start`, `query`, `import` and `export` too.
- Move a collector set between machines with an XML file:
  `logman export Baseline -xml baseline.xml`, then on the target `logman import Baseline -xml baseline.xml`.

## Schedule
`-b` and `-e` set begin and end times (format `M/d/yyyy h:mm:ss[AM|PM]`) and `-r` repeats the collector daily at those times;
`-m` switches to manual start/stop. Apply to an existing set with `logman update counter ...`.

## Trace sets
`logman query providers` lists the data collector providers on the system.

## Analyse
```
relog <log>.blg -f csv -o baseline.csv
relog <log>.blg -b "M/D/YYYY HH:MM:SS" -e "M/D/YYYY HH:MM:SS" -o slice.blg
```
`relog` copies counters from every record of the input log, converting the format if necessary; `-f` accepts
`bin`, `csv`, `tsv` or `SQL` (default `bin`); `-t n` keeps every nth sample; `-q` lists the counters and time
range of a log. Open `.blg` files in Performance Monitor.

## Verify
- [ ] Collector running after the planned restart/schedule; logs not filling the system drive.

## Checked
2026-10-28. Confirmed against the Learn pages for `logman create counter`, `logman import/export`, `logman query`, `logman start/stop` and `relog` (all options listed above, formats, 2 GB csv limit, `-max` in MB). Removed as unconfirmed: the counter-path list, default PerfLogs folder, interval guidance, built-in set report timing, alert-set example and PAL.
Method: documentation only; no commands were run.
