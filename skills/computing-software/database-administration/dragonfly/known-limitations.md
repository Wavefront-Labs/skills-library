---
id: computing-software.database-administration.dragonfly.known-limitations
name: known-limitations
category: computing-software
field: database-administration
product: dragonfly
tags: [limits, max-keys, ttl-range, max-multi-bulk-len, dragonfly]
level: intro
status: docs-checked
description: "Know Dragonfly's hard limits: keys per thread, collection sizes, TTL range, arguments per command and string size."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/known-limitations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Limits documented for Dragonfly:

- Keys: up to two billion keys per CPU thread.
- Lists, sets and hashes: up to two billion values each.
- TTL: 32-bit, about 136 years (rounded down).
- Arguments per command: up to 2^16, configurable via `max_multi_bulk_len`.
- Arguments and strings: up to 256MB.

Related defaults: `maxclients` 64000, `dbnum` 16, `keys_output_limit` 8192.

## Checked

2026-11-04. Confirmed in the Known Limitations page (all five limits) and the flags page (`maxclients`, `dbnum`, `keys_output_limit` defaults). Nothing removed.

Method: documentation only; no commands were run.
