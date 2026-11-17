---
id: computing-software.software-engineering.erlang.node-connections
name: node-connections
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-distribution, node-connections]
level: practitioner
status: docs-checked
description: "Distributed Erlang: sname vs name, automatic and transitive connections, nodes(), net_ticktime, net_kernel:start at runtime."
sources:
  - https://www.erlang.org/doc/system/distributed.html
  - https://www.erlang.org/doc/apps/kernel/net_kernel.html
  - https://www.erlang.org/doc/apps/kernel/kernel_app.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nodes and connections
**Goal:** name nodes correctly and understand how they connect.

```
erl -sname a -setcookie secret
erl -name b@host.example.org -setcookie secret
```
```erlang
net_adm:ping('a@host'),
nodes(),
net_kernel:start([dilbert, shortnames]).
```
- A node is a runtime given a name with `-name` (long names, full host name) or `-sname` (short names, first part of the host name); the form is `name@host` and `node()` returns it. An unnamed node is `nonode@nohost`; `net_kernel:start/1` can name it at runtime.
- A node with a long name cannot communicate with a node with a short name.
- Connections are made lazily, the first time another node's name is used, for example by `spawn(Node, M, F, A)` or `net_adm:ping(Node)`.
- Connections are transitive by default: if A connects to B and B is connected to C, A also tries to connect to C. `-connect_all false` turns this off.
- When a node goes down its connections are removed; `erlang:disconnect_node(Node)` forces a disconnect. `nodes()` lists the visible connected nodes; hidden nodes are not in the list and are not tracked by `global`.
- `net_ticktime` (kernel parameter) is the approximate time a connected node may be unresponsive before it is considered down; it defaults to 60 seconds, with `net_tickintensity` defaulting to 4.

## Gotchas
- Cookies must match for a connection to be accepted (see epmd-cookies).
- Transitive connection makes a full mesh by default; use hidden nodes or `-connect_all false` for client-style nodes.

## Self-check
Start two nodes on one machine, `net_adm:ping/1` between them and check `nodes()` on both.

## Checked
Method: docs-checked 2026-11-09 against the Erlang Distributed Erlang page (nodes, node connections), the net_kernel page (name domains) and the kernel application page (net_ticktime, net_tickintensity). Dropped the erpc/rpc claims, the pang troubleshooting note, message-ordering and large-message claims, which these pages do not cover.
