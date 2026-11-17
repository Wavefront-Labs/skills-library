---
id: computing-software.cloud-infrastructure-engineering.nginx.binary-upgrade-usr2
name: binary-upgrade-usr2
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, binary-upgrade, usr2, upgrade-executable, winch, zero-downtime]
level: advanced
status: docs-checked
description: "Upgrading the nginx binary on the fly with USR2, WINCH and QUIT, and how to roll back with HUP or TERM."
sources: ["https://nginx.org/en/docs/control.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

nginx can replace its executable without dropping connections. Put the new executable file in place of the old one, then send `USR2` to the master process.

1. The master renames its pid file to the same name with a `.oldbin` suffix (for example `nginx.pid.oldbin`) and starts the new executable, which starts new workers. The pid file location is `logs/nginx.pid` under the prefix by default and can be changed with the `pid` directive.
2. Old and new workers all keep accepting requests.
3. Send `WINCH` to the old master: it asks its workers to shut down gracefully, and after a while only the new workers serve requests.
4. If the upgrade is good, send `QUIT` to the old master and only the new processes stay.

The old master does not close its listen sockets, so it can start workers again. If the new executable misbehaves, either:

- send `HUP` to the old master (it starts new workers without re-reading the configuration), then send `QUIT` to the new master; or
- send `TERM` to the new master, which tells its workers to exit immediately (send `KILL` to any that do not); when the new master exits, the old master starts new workers automatically and removes the `.oldbin` suffix from its pid file name.

To preserve established QUIC connections during an upgrade or reload, `quic_bpf` should be enabled.

## Checked

2026-11-03. Confirmed against the nginx "Controlling nginx" page (signals, `.oldbin` pid file, WINCH, rollback options, QUIC note). Removed: the shell script with invented paths, claims about dynamic module mismatches, systemd wrappers and `nginx -s upgrade`, and the invented Verify step.
Method: documentation only; no commands were run.
