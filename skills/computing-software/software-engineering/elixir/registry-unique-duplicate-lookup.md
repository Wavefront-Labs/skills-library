---
id: computing-software.software-engineering.elixir.registry-unique-duplicate-lookup
name: registry-unique-duplicate-lookup
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, registry, unique-keys, duplicate-keys, registry-lookup, registry-dispatch, registry-select, registry-usage, elixir-registry]
level: practitioner
status: docs-checked
description: "Use Registry for process naming (unique) and pub/sub style fan-out (duplicate), with lookup, register and dispatch."
sources: ["https://hexdocs.pm/elixir/Registry.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Registry: unique and duplicate keys

**Goal:** find processes by key without atoms.

```elixir
{Registry, keys: :unique, name: MyApp.Registry}            # in the supervision tree
{:ok, _} = Registry.register(MyApp.Registry, "room:1", metadata)   # registers the CALLING process
Registry.lookup(MyApp.Registry, "room:1")                   #=> [{pid, metadata}]
Registry.unregister(MyApp.Registry, "room:1")

{Registry, keys: :duplicate, name: MyApp.Subs, partitions: System.schedulers_online()}
Registry.register(MyApp.Subs, :topic, nil)
Registry.dispatch(MyApp.Subs, :topic, fn entries -> for {pid, _} <- entries, do: send(pid, :event) end)
Registry.count(MyApp.Registry) ; Registry.select(MyApp.Registry, [{{:"$1", :_, :_}, [], [:"$1"]}])
```

## Rules
- `register/3` registers the calling process; with `keys: :unique` a second register of the same key returns `{:error, {:already_registered, pid}}`.
- If a registered process crashes its keys are removed automatically, but the change may not propagate immediately, so lookups can return dead processes.
- A Registry is local and non-distributed.
- `partitions:` defaults to 1; for highly concurrent workloads the docs suggest `System.schedulers_online()`.

## Self-check
Register two processes under a duplicate key and `dispatch` to both.

## Checked
2026-11-03: confirmed against the Registry docs (`register/3` returning `{:error, {:already_registered, pid}}` for unique keys, `lookup/2`, `dispatch/4`, `count/1`, `select/2`, `partitions` option and scheduler suggestion, crash cleanup, local non-distributed scope). Removed: the `:global`/`:pg` cluster advice (not in the Registry docs).
Method: documentation only; no commands were run.
