---
id: computing-software.software-engineering.erlang.crash-dumps
name: crash-dumps
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-debugging, crash-dumps]
level: practitioner
status: draft
description: "Erlang crash dumps: where erl_crash.dump goes, ERL_CRASH_DUMP, slogan and crashdump_viewer."
sources:
  - https://www.erlang.org/doc/apps/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# erl_crash.dump analysis
**Goal:** diagnose why the VM died.

- When the VM crashes (out of memory, atom table full, fatal error) it writes `erl_crash.dump` to the working directory, or the path in the `ERL_CRASH_DUMP` environment variable (limit time with `ERL_CRASH_DUMP_SECONDS`).
- The first line of the file has a `Slogan:` with the cause, for example `eheap_alloc: Cannot allocate ... bytes of memory`.
- Analyse: `crashdump_viewer:start()` (needs wx) shows processes, memory, ETS and ports; the largest message queues and heaps usually point to the culprit.
- Containers: mount a volume for the dump path or you lose it on restart.
- Disable dumps on small disks with `ERL_CRASH_DUMP_SECONDS=0`.

## Gotchas
- A dump can be large and contain secrets from memory; protect it.

## Self-check
In a throwaway VM, call `erlang:halt("test")` (it writes a dump with that slogan) and read the Slogan line of the file.
