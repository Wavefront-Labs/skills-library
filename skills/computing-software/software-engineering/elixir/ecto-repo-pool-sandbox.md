---
id: computing-software.software-engineering.elixir.ecto-repo-pool-sandbox
name: ecto-repo-pool-sandbox
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, ecto-repo, pool-size, ecto-sandbox, checkout, db-connection, queue-target, postgrex, ecto-repo-config]
level: practitioner
status: docs-checked
description: "Configure Repo (url, pool_size, timeouts), start it in the supervision tree and use Ecto.Adapters.SQL.Sandbox for isolated async tests."
sources: ["https://hexdocs.pm/ecto/Ecto.Repo.html", "https://hexdocs.pm/ecto_sql/Ecto.Adapters.SQL.Sandbox.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repo configuration, pooling and sandbox testing

**Goal:** reliable DB connections in prod and isolated DB state in tests.

```elixir
# runtime.exs
config :my_app, MyApp.Repo, url: System.fetch_env!("DATABASE_URL"), pool_size: 10, ssl: true
# config/test.exs
config :my_app, MyApp.Repo, pool: Ecto.Adapters.SQL.Sandbox, pool_size: 10
# test_helper.exs
Ecto.Adapters.SQL.Sandbox.mode(MyApp.Repo, :manual)
# DataCase setup
setup tags do
  pid = Ecto.Adapters.SQL.Sandbox.start_owner!(MyApp.Repo, shared: not tags[:async])
  on_exit(fn -> Ecto.Adapters.SQL.Sandbox.stop_owner(pid) end)
  :ok
end
```

## Rules
- Each sandbox test runs in a transaction that is rolled back; allow other processes with `Ecto.Adapters.SQL.Sandbox.allow` or shared mode in non-async tests.
- Total pool sizes across nodes must stay under the database's connection limit.

## Self-check
Run two async tests that insert the same unique row and confirm they do not collide.

## Checked
2026-11-08: confirmed against Ecto.Repo (pool_size config) and Ecto.Adapters.SQL.Sandbox (mode, start_owner!, stop_owner, allow, shared mode). Removed: queue_target and queue_interval, the schedulers_online pool size, the connection-not-available error text and the ecto_repos advice.
Method: documentation only; no commands were run.
