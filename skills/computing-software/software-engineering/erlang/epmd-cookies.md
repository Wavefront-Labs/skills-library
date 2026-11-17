---
id: computing-software.software-engineering.erlang.epmd-cookies
name: epmd-cookies
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-distribution, epmd-cookies]
level: advanced
status: docs-checked
description: "Erlang distribution plumbing: epmd on port 4369, listen port range, magic cookie file and firewall rules."
sources:
  - https://www.erlang.org/doc/system/distributed.html
  - https://www.erlang.org/doc/apps/erts/epmd_cmd.html
  - https://www.erlang.org/doc/apps/kernel/kernel_app.html
  - https://www.erlang.org/doc/apps/erts/erl_cmd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# epmd, cookies and ports
**Goal:** open the right ports and manage the cookie.

- `epmd` (Erlang Port Mapper Daemon) is a name server that maps node names to the addresses (ports) of nodes on its host. It listens on TCP 4369 by default (`-port` or `ERL_EPMD_PORT` changes it) and is started automatically by `erl` for a distributed node if none is running.
- Fix the distribution port range with the kernel parameters `inet_dist_listen_min` and `inet_dist_listen_max`, for example `erl -kernel inet_dist_listen_min 9100 inet_dist_listen_max 9105` (also settable in `sys.config` under `kernel`).
- Cookie: a node's magic cookie is an atom; on connect the cookies are compared and a mismatch rejects the connection. The default cookie comes from `.erlang.cookie` in the user's home directory, created with a random string and permission mode 400 if absent. Set it with `-setcookie Cookie` (or `erlang:set_cookie/1`).
- Firewall: epmd answers port and name-listing queries from remote hosts and refuses registrations from them; the guide says firewall software must be used to restrict access further. `-address` limits the addresses epmd listens on.
- `epmd -names` lists the names registered with the running epmd. `-no_epmd` says the node needs no epmd at all; `-epmd_module` is deprecated in favour of the kernel `epmd_module` parameter.

## Gotchas
- The cookie is "security" only against accidental misuse, such as a node joining the wrong cluster, not cryptographic security; the guide notes inter-node traffic is clear text by default and points to TLS for Erlang distribution when strong security is needed.
- Nodes with identical cookie files communicate freely; protect and distribute the cookie like a secret.

## Self-check
Verify with `epmd -names` after starting a node, then restrict ports and retest.

## Checked
Method: docs-checked 2026-11-09 against the Erlang Distributed Erlang reference page (security, cookies), the epmd command page, the kernel application page (inet_dist_listen_min/max, epmd_module) and the erl command page (-setcookie, -no_epmd). Dropped the claim that a cookie holder can run arbitrary code and the container-image advice, which these pages do not state.
