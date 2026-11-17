---
id: computing-software.systems-network-administration.icinga-2.plugin-api-output-status-and-thresholds
name: plugin-api-output-status-and-thresholds
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, plugin-api, exit-codes, threshold-ranges, timeout, verbose, plugin-development]
level: advanced
status: docs-checked
description: Write plugins to the Icinga 2 and Monitoring Plugins API - output format, exit statuses 0-3, threshold order and range syntax with @ and ~, timeout, version and verbose flags.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/05-service-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# plugin API: output, status and thresholds
Icinga 2 supports the Monitoring Plugins plugin API.

**Output:** `<STATUS>: <short description>`, e.g. `WARNING: MySQL connection time is slow (0.5s > 0.1s threshold)`. Multi-line output is supported: Icinga Web shows the first line in listings and everything in the detail view. Implement `--verbose` for extra debug output.

**Exit status:** 0 OK, 1 Warning, 2 Critical, 3 Unknown (invalid parameters and low-level resource errors preventing the check). These are service states; Icinga maps host state itself.

**Thresholds:** evaluate critical first (it supersedes), then warning, else OK. Never hardcode values; take `-w/--warning` and `-c/--critical` arguments and check they were given before comparing, since users may pass only critical.

**Ranges** use `[@]start:end`:
- `start <= end`, otherwise error (`30:10`)
- `start:` may be omitted when 0 (`10` alerts outside 0..10)
- omitted `end` means infinity (`10:` alerts below 10)
- `~` is negative infinity (`~:10` alerts above 10)
- `10:20` alerts outside 10..20
- `@10:20` alerts inside 10..20, inclusive

Implement single values or fully support ranges, ideally with an existing library.

**Timeout:** Icinga kills long-running processes (timeout set on the CheckCommand or the host/service), but best practice is to handle it in the plugin and return a clear message with Unknown (3).

**Version and verbose:** provide `-V/--version` and `-v/--verbose`, and add verbose handling before the check logic.

## Checked

2026-11-04. Confirmed against the Icinga 2 service monitoring chapter: plugin output format, multi-line output, exit codes, threshold range syntax including the ~ character, -V/--version and -v/--verbose recommendations.

Method: documentation only; no commands were run.
