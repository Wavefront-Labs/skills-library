---
id: computing-software.software-engineering.deno.permission-broker
name: permission-broker
category: computing-software
field: software-engineering
product: deno
tags: [permissions, permission-broker, policy, unix-socket, named-pipe, json-schema]
level: sme
status: docs-checked
description: "Delegate all Deno permission checks to an external broker via DENO_PERMISSION_BROKER_PATH: behaviour, failure mode and request/response message shape."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/security.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Advanced use only. Set `DENO_PERMISSION_BROKER_PATH` to a Unix domain socket path (e.g. `/tmp/deno-perm.sock`) or, on Windows, a named pipe (e.g. `\\.\pipe\deno-perm-broker`).

While a broker is active:

- All `--allow-*` and `--deny-*` flags are ignored.
- Prompts are not shown (like non-interactive mode).
- Every permission check goes to the broker, which must answer each one.

If anything goes wrong (cannot connect, malformed or out-of-order messages, ID mismatch, connection closed), Deno immediately terminates the process to prevent escalation. Make the broker resilient, audited and available.

Messages are versioned and defined by JSON Schemas (`permission-broker-request.v1.json`, `permission-broker-response.v1.json` in denoland/deno `cli/schemas`). A request carries `v`, `pid`, a unique monotonic `id`, `datetime` (RFC 3339), `permission` and an optional `value`. The response echoes `id` with `result` of `"allow"` or `"deny"`, plus an optional `reason`.

```text
-> req {"v":1,"pid":10234,"id":5,"datetime":"2025-01-01T00:00:04.000Z","permission":"env","value":null}
<- res {"id":5,"result":"deny","reason":"Environment access is denied."}
```

## Checked

2026-11-04. Confirmed against docs runtime/fundamentals/security.md: DENO_PERMISSION_BROKER_PATH, socket and pipe examples, behaviour while active, failure mode, message fields and result values.

Method: documentation only; no commands were run.
