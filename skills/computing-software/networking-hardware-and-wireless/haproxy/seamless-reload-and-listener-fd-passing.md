---
id: computing-software.networking-hardware-and-wireless.haproxy.seamless-reload-and-listener-fd-passing
name: seamless-reload-and-listener-fd-passing
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, seamless-reload, expose-fd-listeners, master-worker-mode, hard-stop-after, reload-sigusr2]
level: practitioner
status: docs-checked
description: "Reload HAProxy with master-worker mode and listener fd passing (-x, expose-fd listeners), SIGUSR2, hard-stop-after and show proc for old workers."
sources:
  - https://docs.haproxy.org/3.0/management.html
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# seamless reload and listener fd passing
```
global
    master-worker
    stats socket /var/run/haproxy.sock mode 600 level admin expose-fd listeners
    hard-stop-after 30m
```
- Master-worker mode (`master-worker` in `global`, or `-W`; `-Ws` for a systemd `notify` service, which needs a `USE_SYSTEMD` build) starts a master that forks workers and monitors them. Send `SIGUSR2` to the master to reload: it re-reads the configuration and forks a new worker, and the previous worker stays until it finishes its jobs. By default a worker exiting with a bad return code kills all workers and the master leaves (`no-exit-on-failure` changes that).
- Reload via the master CLI: `reload` does the same as `kill -USR2`, needs `operator` or `admin` level, and is synchronous, returning `Success=1` or `Success=0` with the loading messages. `socat` times out after 0.5 s by default, so use `-t300` (for example `echo "reload" | socat -t300 /var/run/haproxy-master.sock stdin`). `reload` must be the last command on the line and closes all master CLI connections.
- Listener fd passing: `-x <unix_socket>` makes the new process fetch the listening sockets from the old process instead of binding new ones, avoiding missed connections on Linux. Without master-worker mode the stats socket needs `expose-fd listeners`. In master-worker mode it is not needed: the master uses `-x` automatically with the `sockpair@` syntax; pass `-x /dev/null` to disable.
- Without that, the old way is `-sf <pid>` (graceful: SIGUSR1 tells old processes to stop listening and exit when their connections close) or `-st` (hard: SIGTERM). If a bind fails because the port is in use, the new process sends SIGTTOU to pause old listeners and SIGTTIN to resume them if it still fails. The manual notes two windows of a few milliseconds where connection failures can occur under load, typically about 1 per 10000 new connections per second per reload.
- `hard-stop-after <time>` is the maximum time a soft-stop may last (default unit milliseconds), forcing old processes out even if connections stay open. It applies in TCP and HTTP mode.
- `show proc` on the master CLI lists the master (with reload count), workers and old workers, plus programs. An old worker that survived several reloads shows up under `# old workers`, and you can reach its CLI to see why.

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 management guide (command-line options `-W`, `-Ws`, `-sf`, `-x`; the reload and signal description; master CLI `reload` and `show proc`) and configuration manual (`master-worker`, `hard-stop-after`, `expose-fd listeners`). Removed: the SO_REUSEPORT claim, the lists of what survives or resets across a reload (stick tables, server states, counters), the `systemctl` command lines, the memory advice, and the curl loop verification. Read as sections of both documents only.
Method: documentation only; no commands were run.
