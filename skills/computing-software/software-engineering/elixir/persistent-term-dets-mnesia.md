---
id: computing-software.software-engineering.elixir.persistent-term-dets-mnesia
name: persistent-term-dets-mnesia
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, persistent-term, dets, mnesia, ets-vs-agent, cachex, in-memory-cache, ets-alternatives]
level: advanced
status: docs-checked
description: "Pick persistent_term for rarely-changing read-mostly config, ETS for mutable caches, DETS/Mnesia for persistence, and know their limits."
sources: ["https://www.erlang.org/doc/apps/erts/persistent_term.html", "https://www.erlang.org/doc/apps/mnesia/mnesia.html", "https://www.erlang.org/doc/apps/stdlib/dets.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# persistent_term, DETS and Mnesia choices

**Goal:** choose the storage primitive that matches the access pattern.

```elixir
:persistent_term.put({MyApp, :config}, %{limit: 10})
:persistent_term.get({MyApp, :config}) ; :persistent_term.get(key, default)
:persistent_term.erase({MyApp, :config})

{:ok, d} = :dets.open_file(:store, file: ~c"/var/data/store.dets", type: :set)   # path is a charlist
:dets.insert(:store, {:k, 1}) ; :dets.lookup(:store, :k) ; :dets.close(:store)
```

## Rules
- `persistent_term`: very fast reads, no copy; writes and erasures trigger a global garbage collection scan, so use for data updated rarely (startup config, compiled routing tables).
- ETS: mutable, concurrent, in memory only, per-node.
- DETS: disk-based, file size cannot exceed 2 GB. Mnesia: distributed database with transactions. For general persistence use a real database through Ecto.

## Self-check
Why is updating a persistent_term in a hot path a bad idea? Each update forces a scan of all processes.

## Checked
2026-11-08: confirmed against the Erlang persistent_term page (global garbage collection pass scanning all processes on update or erase), the dets page (2 GB size limit) and the mnesia page. Removed: the claim that DETS is slow, the Mnesia schema-setup remark, the niche remark and the caching-library advice.
Method: documentation only; no commands were run.
