---
id: computing-software.networking-hardware-and-wireless.bind9.rndc-server-and-cache-commands
name: rndc-server-and-cache-commands
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, rndc, status, flush, dumpdb]
level: practitioner
status: docs-checked
description: "rndc commands that control a running BIND 9 server: status, reconfig, flush, dumpdb, querylog, recursing, stats, stop and halt."
sources:
  - https://bind9.readthedocs.io/en/latest/manpages.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rndc server and cache commands
Server-level `rndc` commands:

- `status` shows server state; `reconfig` reloads only the configuration and new zones; `reload` also reloads changed zone files.
- `stop -p` and `halt -p` shut down (`stop` saves recent dynamic-update and IXFR changes to the zone files first, `halt` does not); `-p` returns named's process ID.
- `flush`, `flushname name`, `flushtree name` clear cache data.
- `dumpdb` writes the cache to a file.
- `querylog` toggles query logging; `recursing` lists active recursive queries.
- `stats` writes the statistics file; `reset-stats` clears counters.
- `fetchlimit` and `tcp-timeouts` inspect limits and timers.
- `closelogs` closes the open log files, for use by external log rotation.
- `serve-stale` controls stale answers; `nta` manages negative trust anchors; `secroots` dumps security roots.
- `showconf` prints the running configuration (`-user`, `-builtin` or `-effective`).

## Checked

2026-11-04. Confirmed against the rndc section of the named man pages: each listed command exists with the described purpose. Clarified `stop` versus `halt` and `closelogs`.

Method: documentation only; no commands were run.
