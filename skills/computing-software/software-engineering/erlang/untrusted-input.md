---
id: computing-software.software-engineering.erlang.untrusted-input
name: untrusted-input
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-security, untrusted-input]
level: sme
status: draft
description: "Erlang input hardening: binary_to_term safe, list_to_existing_atom, atom exhaustion, process and mailbox limits."
sources:
  - https://www.erlang.org/doc/apps/crypto/
  - https://www.erlang.org/doc/apps/ssl/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Safe handling of untrusted terms
**Goal:** avoid VM-level denial of service from external data.

```erlang
Term = binary_to_term(Bin, [safe]),          % rejects unknown atoms, funs, etc.
Atom = binary_to_existing_atom(Name, utf8),  % never create atoms from input
```
- Atoms are never freed; creating them from input can crash the VM (default limit 1048576).
- `binary_to_term/1` on attacker data can create funs or atoms; prefer a text format (JSON) for external protocols and use `[safe]` for internal ones.
- Bound everything: message sizes, queue length (`process_flag(message_queue_data, off_heap)` plus checks), `max_heap_size` per process, connection counts, request body size.
- `spawn_opt(F, [{max_heap_size, #{size => 10000000, kill => true}}])` kills runaway processes.

## Gotchas
- `os:cmd/1` with interpolated input is shell injection.

## Self-check
Feed a crafted atom-creating binary to `binary_to_term(Bin, [safe])` and confirm it raises.
