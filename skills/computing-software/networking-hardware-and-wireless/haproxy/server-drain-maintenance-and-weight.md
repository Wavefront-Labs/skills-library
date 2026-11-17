---
id: computing-software.networking-hardware-and-wireless.haproxy.server-drain-maintenance-and-weight
name: server-drain-maintenance-and-weight
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, set-server-state, drain, maint, set-weight, disable-server, ready]
level: practitioner
status: docs-checked
description: "Gracefully drain or disable a HAProxy server and change weight or address at runtime with the set server, set weight and shutdown sessions commands."
sources:
  - https://docs.haproxy.org/3.0/management.html
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# server drain maintenance and weight
These commands are sent to the runtime API (stats socket) and need a socket configured for level `admin`. Backend and server may be given by name or by numeric ID prefixed with `#`.

```
set server be_app/a state drain
show servers conn be_app
shutdown sessions server be_app/a
set server be_app/a state maint
set server be_app/a state ready
set server be_app/a weight 25%
set server be_app/a addr 10.0.0.99 port 8080
```
- `state drain` removes the server from load balancing but it is still checked and still accepts new persistent connections, so sticky clients keep reaching it.
- `state maint` stops all traffic and all health checks (the same as `disable server`); the stats page shows `MAINT`, and servers tracking it show `MAINT(via)`. `state ready` returns to normal (the same as `enable server`).
- `shutdown sessions server` immediately terminates all streams on the server, as is useful after putting it into maintenance; they are logged with the `K` flag.
- `show servers conn` dumps current and idle connections per server; the docs describe it as a debugging tool, not for routine monitoring.
- `set server ... weight <weight>[%]` equals `set weight`. Absolute weights run from 0 to 256; a `%` value is relative to the initial weight and capped at 256. Servers in a farm using a static balance algorithm accept only 0 and 100% (or the initial weight). Setting weight to zero during an update and back to 100% afterwards is the documented typical use. Changes take effect immediately, though some algorithms need requests to pass before the change shows.
- `set server ... addr <ip> [port <port>]` replaces the address; `check-addr`/`check-port` and `agent-addr`/`agent-port` change check targets.

Persisting state across a reload: write the output of `show servers state` to the file named by the global `server-state-file` (relative paths use `server-state-base`); at startup HAProxy loads the state of each server found in the file. Loading is enabled by the `load-server-state-from-file` keyword described in the configuration manual.

Verify: `show servers state be_app` lists `srv_admin_state` as a bit mask (0x01 forced maintenance, 0x08 forced drain) and `srv_uweight` for the weight.

## Checked
2026-11-03. Confirmed against management.html (`set server` forms, `set weight`, `disable server`, `enable server`, `shutdown sessions server`, `show servers conn`, `show servers state`) and configuration.html (`server-state-file`, `server-state-base`). Fixed: the weight limit is 256 absolute (not 256 times the initial weight) and static-algorithm farms accept only 0 and the initial weight; drain admin-state value is 0x08 forced drain, forced maintenance 0x01 (not "8 and 1" as plain codes); `load-server-state-from-file` was wrongly shown as a global keyword. Removed: `socat` usage, "weight 0 is a drain without health-state change", and the "stats page shows DRAIN" claim.
Method: documentation only; no commands were run.
