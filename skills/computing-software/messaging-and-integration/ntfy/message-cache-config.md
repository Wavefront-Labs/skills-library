---
id: computing-software.messaging-and-integration.ntfy.message-cache-config
name: message-cache-config
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, message-cache, cache-file, cache-duration, persistence]
level: practitioner
status: docs-checked
description: "Configure the ntfy message cache: in-memory default, persistent cache-file, cache-duration, and batching for busy servers."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message cache

By default messages stay in memory for 12 hours and do not survive a restart.

```yaml
cache-file: "/var/cache/ntfy/cache.db"
cache-duration: "12h"
```

- `cache-file` (SQLite) or `database-url` (PostgreSQL) makes the cache persistent.
- `cache-duration` defaults to `12h`; `0` disables the cache.
- Clients fetch cached messages with `poll=1` or `since=`.

## Busy servers

```yaml
cache-batch-size: 25
cache-batch-timeout: "1s"
```

Batch writes; defaults are 0 (off). `cache-startup-queries` can enable WAL mode.

## Gotchas

- With the cache disabled, messages go only to connected subscribers and are never stored, so `since=` and `poll=1` cannot return them.
- Attachment expiry is capped at `cache-duration`.

## Checked

2026-11-04. Confirmed against the ntfy config page (Message cache, Tuning for scale, config table): in-memory 12h default, restart behaviour, `cache-file`, `database-url`, `cache-duration` 12h and 0, batch options with default 0, ntfy.sh example values, WAL via `cache-startup-queries`, attachment cap. Removed: scheduled-delivery and catch-up claims, a directory-permission line and the Verify step.
Method: documentation only; no commands were run.
