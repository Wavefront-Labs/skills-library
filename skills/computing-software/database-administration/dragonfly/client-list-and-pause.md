---
id: computing-software.database-administration.dragonfly.client-list-and-pause
name: client-list-and-pause
category: computing-software
field: database-administration
product: dragonfly
tags: [client-list, client-pause, client-kill, maxclients, dragonfly]
level: practitioner
status: docs-checked
description: "List connections with CLIENT LIST filters and pause clients with CLIENT PAUSE in WRITE or ALL mode, plus connection limit flags."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/server-management/info.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/server-management/client-list.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/server-management/client-pause.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/compatibility.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## CLIENT LIST

```
CLIENT LIST [TYPE <type>] [ID <client-id> [client-id ...]]
```

`TYPE` and `ID` are mutually exclusive. Output is one connection per line of `property=value` fields: `id`, `addr`, `laddr`, `fd`, `name` (from `CLIENT SETNAME`), `age`, `idle`, `phase`. New fields appear regularly, so parse defensively and skip unknown ones.

## CLIENT PAUSE

```
CLIENT PAUSE timeout [WRITE | ALL]
```

Suspends clients for `timeout` milliseconds. `ALL` (default) blocks all client commands; `WRITE` blocks only clients that try a write. It returns `OK` immediately and the pause itself is not paused. Replica interactions continue. When the time has elapsed, clients are unblocked and the commands accumulated in each client's query buffer during the pause are processed.

## Limits

- `--maxclients` (default 64000) caps concurrent clients; refusals appear as `rejected_connections` in `INFO stats`.
- `--timeout` closes idle connections after N seconds (0 disables).

Compatibility table: `CLIENT KILL` lacks MAXAGE, SKIPME and USER; `CLIENT NO-EVICT`, `NO-TOUCH`, `REPLY` and `UNBLOCK` are unsupported.

## Checked

2026-11-04: confirmed against the CLIENT LIST and CLIENT PAUSE command pages, the compatibility table, the flags page (`--maxclients`, `--timeout`) and the INFO page (`rejected_connections`). Removed the unstated advice to use `CLIENT UNPAUSE` early.
Method: documentation only; no commands were run.
