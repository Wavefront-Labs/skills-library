---
id: computing-software.networking-hardware-and-wireless.frrouting.exec-mode-diagnostics
name: exec-mode-diagnostics
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, show-memory, show-event, cputime-warning, walltime-warning, find, yang]
level: practitioner
status: docs-checked
description: "FRR exec-mode diagnostics: memory, RCU and event statistics, CPU and wall-time warnings, command search with find, YANG data views and the include pipe."
sources:
  - https://docs.frrouting.org/en/latest/basic.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exec-mode diagnostics
- `who` lists vty sessions; `list` lists commands; `show version`, `show history`, `show motd`.
- `show memory [DAEMON] [json]`, `show rcu [json]`.
- `show event cpu [r|w|t|e|x]` run statistics by event type (read, write, timer, event, execute); `show event poll`; `show event timers`.
- `show configuration running [<json|xml> [translate WORD]] [with-defaults] DAEMON` shows running YANG configuration.
- `show yang operational-data XPATH [{format <json|xml>|translate TRANSLATOR|with-config}] DAEMON`.
- `find REGEX...` searches all commands in all modes and shows the mode of each match (POSIX extended regex; repeated spaces collapse, use `\s` for more).
- Pipe filter: `... | include REGEX`; do not quote the regex.

Slow-handler warnings:
- `service cputime-stats` is enabled by default; disabling it makes `cputime-warning` non-functional.
- `service cputime-warning (1-4294967295)` warns when a handler or CLI command exceeds the limit in ms.
- `service walltime-warning (1-4294967295)` warns on total wall-clock time in ms; it includes I/O wait so it can be noisy under load.

`show tcmalloc stats` and `memory release rate (0-100)` exist only when built with tcmalloc.

## Checked

2026-11-04. Confirmed against the FRR Basic Commands page: exec-mode show commands, find, include pipe, cputime and walltime warnings, tcmalloc commands. Nothing changed.
Method: documentation only; no commands were run.
