---
id: computing-software.messaging-and-integration.ntfy.logging-config
name: logging-config
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, logging, log-level, log-format, debug]
level: practitioner
status: docs-checked
description: "Configure ntfy server logging: level, format, file, per-tag overrides and hot reload."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging

```yaml
log-level: debug
log-format: json
log-file: /var/log/ntfy.log
log-level-overrides:
  - "tag=manager -> trace"
```

- `log-format`: `text` (default) or `json`.
- `log-file`: unset means stderr.
- `log-level`: `trace`, `debug`, `info` (default), `warn`, `error`.
- `log-level-overrides` entries look like `tag=manager -> trace`.

## Quick toggles

- Env var: `NTFY_LOG_LEVEL=debug` (or `trace`).
- Flags: `ntfy serve --debug` or `--trace`.
- systemd: `journalctl -u ntfy -f`.

## Hot reload

Only `log-level` and `log-level-overrides` hot reload: edit `server.yml`, then `systemctl reload ntfy` or `kill -HUP <pid>`.

## Gotchas

- `debug` and `trace` are very verbose, and `log-level-overrides` has a performance penalty; use them only briefly.
- `debug` logs information about each published message but not its contents; `trace` also prints the contents.

## Checked

2026-11-04. Confirmed against the ntfy config page (Logging and debugging, config table, flags) and troubleshooting page (`journalctl -u ntfy -f`): keys, defaults, level list, override syntax, env var and flags, hot reload scope. Corrected: hot reload covers only the two log options. Removed: a hosted-logs claim and the Verify step.
Method: documentation only; no commands were run.
