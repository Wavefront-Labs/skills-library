---
id: computing-software.systems-network-administration.headscale.logging-config
name: logging-config
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, log-level, debug, trace, database-debug]
level: intro
status: docs-checked
description: "Set Headscale's log level and format, enable database query logging, and know which levels are valid."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/debug.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging

```yaml
log:
  level: info
  format: text
```

- Valid levels: panic, fatal, error, warn, info, debug, trace.
- Format: `text` or `json`.
- For more output when troubleshooting, set `level: debug` (or `trace`).

## Database query logging

```yaml
database:
  debug: false
```

When enabled it logs all database queries, and requires `log.level` to be `debug` or `trace`.

## Gotchas

- Client-side logs are separate: `tailscale debug daemon-logs` (client-troubleshooting).
- Whether clients send their logs to Tailscale Inc is a different setting, `logtail` (logtail-privacy).

## Checked

2026-11-04. Confirmed against the Headscale debugging page and config-example.yaml: log.level values and default info, log.format text or json, database.debug and its log level requirement, and the client log command. Removed unsourced restart and container-log instructions and a generic noise remark.
Method: documentation only; no commands were run.
