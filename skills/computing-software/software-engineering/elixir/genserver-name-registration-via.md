---
id: computing-software.software-engineering.elixir.genserver-name-registration-via
name: genserver-name-registration-via
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, genserver-name, via-tuple, global-name, registered-name, process-registry, genserver-naming]
level: practitioner
status: docs-checked
description: "Register servers by local atom name, :global, or {:via, Registry, ...}; choose by whether you need one instance or many."
sources: ["https://hexdocs.pm/elixir/GenServer.html#module-name-registration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Naming and registering GenServers

**Goal:** address processes without passing pids around.

```elixir
GenServer.start_link(Mod, arg, name: Mod)                           # local atom name, one per node
GenServer.start_link(Mod, arg, name: {:global, :my_server})         # cluster-wide
GenServer.start_link(Mod, arg, name: {:via, Registry, {MyReg, key}}) # many instances, any term as key
GenServer.call({:via, Registry, {MyReg, key}}, :req)
GenServer.whereis(Mod) ; Process.whereis(Mod)
```

## Rules
- Atoms are never garbage-collected, so do not generate atom names dynamically; for dynamic local names use a `Registry` with `{:via, Registry, ...}` tuples.
- Starting a duplicate name returns `{:error, {:already_started, pid}}`.
- Wrap `via` construction in a private `via(key)` function, used by client API functions.
- Registry keys of a process that crashes are removed automatically, though the removal may not propagate immediately.

## Checked
2026-11-03: confirmed against the GenServer docs (name registration section: atom, `{:global, term}`, `{:via, module, name}`; `{:error, {:already_started, pid}}`; atoms never garbage-collected; `GenServer.whereis/1`) and the Registry docs (keys removed when the process crashes). Removed: the claim that names are released on every exit (docs say crash, with delayed propagation).
Method: documentation only; no commands were run.

## Self-check
Start two servers with the same atom name and read the `already_started` error.
