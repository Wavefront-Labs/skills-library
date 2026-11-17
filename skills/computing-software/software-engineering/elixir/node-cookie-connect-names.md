---
id: computing-software.software-engineering.elixir.node-cookie-connect-names
name: node-cookie-connect-names
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, node, cookie, distribution, sname, longnames, epmd, net-kernel, node-connect, distributed-nodes, elixir-distribution]
level: advanced
status: docs-checked
description: "Start named nodes with --sname/--name, share the cookie, connect with Node.connect, send messages across nodes and know the security model."
sources: ["https://hexdocs.pm/elixir/Node.html", "https://www.erlang.org/doc/system/distributed.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nodes, cookies and connecting

**Goal:** connect BEAM nodes and use them safely.

```bash
iex --sname a@localhost --erl "-setcookie secret" -S mix
iex --name b@host.example --erl "-setcookie secret"
```
```elixir
Node.connect(:"a@localhost") ; Node.list() ; Node.self()
:erpc.call(:"a@localhost", Enum, :sum, [[1, 2, 3]], 5_000)
Node.spawn(:"a@localhost", fn -> IO.puts("hi") end)
send({MyServer, :"a@localhost"}, :msg)
GenServer.call({MyServer, :"a@localhost"}, :req)
```

## Rules
- Nodes with the same cookie can run arbitrary code on each other. Treat the cookie as a secret, keep distribution ports (epmd 4369 plus a dynamic range) private, and use TLS distribution for untrusted networks.
- Names are `name@host`; short names (`--sname`) and long names (`--name`) cannot mix.
- Releases set the cookie via `RELEASE_COOKIE` (see the releases skill).
- Remote calls can fail with `noconnection`; handle with monitors and timeouts.

## Failure modes
- `:pang`/`false` from `Node.connect` is usually a cookie, name or firewall mismatch.

## Self-check
Start two named nodes locally and call `:erpc.call/4` from one to the other.

## Checked
2026-11-08: confirmed against Elixir Node docs (connect, list, spawn, --sname and --name, noconnection) and the Erlang distributed page (-setcookie, long versus short names cannot communicate, epmd, TLS distribution). Removed: the --cookie flag (the documented route is -setcookie) and the :rpc comparison.
Method: documentation only; no commands were run.
