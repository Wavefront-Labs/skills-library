---
id: computing-software.networking-hardware-and-wireless.envoy.hot-restart-and-restarter
name: hot-restart-and-restarter
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, hot-restart, restart-epoch, base-id, drain-time-s, parent-shutdown-time-s, hot-restarter]
level: practitioner
status: docs-checked
description: "Hot restart Envoy without dropping connections, set drain and parent shutdown times, and drive it with the hot-restarter wrapper and RESTART_EPOCH."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/operations/hot_restart.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/operations/hot_restarter.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# hot restart and restarter
Hot restart reloads code and configuration without dropping existing connections during the drain; connections are not transferred, they must finish or be terminated. The two processes talk over unix domain sockets: counters are passed from old to new, gauges too except those marked `NeverImport`. The new process initialises fully (config, initial discovery, health checks) before requesting the listen sockets from the old one, starts listening, then tells the old process to drain. `--drain-time-s` sets drain duration (draining becomes more aggressive over time). Later the new process tells the old to exit after `--parent-shutdown-time-s`, which is independent of drain time and should be set larger.

Process-manager wrapper:
```
hot-restarter.py start_envoy.sh
# start_envoy.sh
exec /usr/sbin/envoy -c /etc/envoy/envoy.yaml --restart-epoch $RESTART_EPOCH --service-cluster web --service-node n1
```
The wrapper sets `RESTART_EPOCH`, which you must pass to `--restart-epoch`. `SIGHUP` hot restarts by re-running the script; `SIGTERM`/`SIGINT` cleanly stop all children; an unexpected child exit stops the wrapper.

Gotchas: with `--use-dynamic-base-id` set it only when epoch is 0, store the id from `--base-id-path`, and pass it as `--base-id` for later epochs. Raise `fs.inotify.max_user_watches` when watching many files. Parent shutdown must exceed drain time. Verify with `GET /hot_restart_version` and the `server.hot_restart_generation` stat.

## Checked
2026-11-03. Confirmed against hot_restart.rst, hot_restarter.rst and the admin /hot_restart_version entry. Removed or corrected: nothing.
Method: documentation only; no commands were run.
