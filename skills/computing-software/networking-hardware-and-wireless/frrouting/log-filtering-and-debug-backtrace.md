---
id: computing-software.networking-hardware-and-wireless.frrouting.log-filtering-and-debug-backtrace
name: log-filtering-and-debug-backtrace
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, log-filter-text, unique-id, backtrace, debug, filtered-file]
level: advanced
status: docs-checked
description: "Filter FRR log output by text, keep message unique IDs for bug reports, get a backtrace for a logged ID, and enable route-map debugging."
sources:
  - https://docs.frrouting.org/en/latest/basic.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log filtering and debug backtrace
- `log filtered-file [FILENAME [LEVEL]]` sets the destination for filtered logs.
- `log filter-text WORD` prints only messages matching the filter, and only on targets set with `log filtered-file`. The filter is not saved to `frr.conf` or shown in `show running-config`.
- `clear log filter-text` clears all filters; `show log-filter` shows current filters per daemon.
- `log unique-id` adds `[XXXXX-XXXXX]` IDs to log text. Enabled by default; `no log unique-id` disables it. Keep it enabled for bug reports.
- `debug unique-id XXXXX-XXXXX backtrace` prints a backtrace for the log message with that ID, including source location and current event handler. It works in and out of configuration mode and is saved to config only if entered in configuration mode. It can slow logging and inflate log files.
- `debug routemap [detail]` enables route-map debugging; `detail` adds reasoning output.

## Checked

2026-11-04. Confirmed against the FRR Basic Commands page: filtered-file, filter-text, clear, show log-filter, unique-id, debug unique-id backtrace and debug routemap. Nothing changed.
Method: documentation only; no commands were run.
