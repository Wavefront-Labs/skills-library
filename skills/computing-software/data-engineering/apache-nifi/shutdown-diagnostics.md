---
id: computing-software.data-engineering.apache-nifi.shutdown-diagnostics
name: shutdown-diagnostics
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, diagnostics, bootstrap-conf, troubleshooting, shutdown]
level: advanced
status: docs-checked
description: "Dump NiFi diagnostics on shutdown: enabled and verbose flags, output directory, file count and size caps, and the graceful shutdown seconds caveat."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnostics on shutdown (bootstrap.conf)

- `nifi.diagnostics.on.shutdown.enabled`: false
- `nifi.diagnostics.on.shutdown.verbose`: false
- `nifi.diagnostics.on.shutdown.directory`: `./diagnostics`
- `nifi.diagnostics.on.shutdown.max.filecount`: 10 (oldest files are deleted past the limit)
- `nifi.diagnostics.on.shutdown.max.directory.size`: 10 MB (oldest files are deleted past the limit)

The admin guide lists these in its bootstrap.conf table, while a later section shows them as nifi.properties lines; check which file your version reads.

In the case of a lengthy diagnostic NiFi may terminate before the command ends; the guide says to set a higher `graceful.shutdown.seconds` in bootstrap.conf (the bootstrap kills the process when that time runs out).

Related monitoring in nifi.properties: `nifi.monitor.long.running.task.schedule` (the guide's example is `1 min`) and `nifi.monitor.long.running.task.threshold` (example `5 mins`) are disabled by default and both must be set to enable the monitor, which the guide warns creates a thread dump on every run; `nifi.performance.tracking.percentage` is 0 (disabled, range 0-100).

Verify: stop NiFi and a new file appears in the diagnostics directory.

## Checked

Confirmed in the NiFi Administration Guide: the five diagnostics keys and defaults (bootstrap properties table and the diagnostics section), the graceful.shutdown.seconds advice, the Long-Running Task Monitor properties and disabled default, and nifi.performance.tracking.percentage default 0 with range 0 to 100.

Method: docs-only read of cited pages, 2026-11-08
