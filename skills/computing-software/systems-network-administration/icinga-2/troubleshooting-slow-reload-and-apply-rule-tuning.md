---
id: computing-software.systems-network-administration.icinga-2.troubleshooting-slow-reload-and-apply-rule-tuning
name: troubleshooting-slow-reload-and-apply-rule-tuning
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, troubleshooting, performance, jemalloc, concurrency, assign-where, reload]
level: advanced
status: docs-checked
description: "Speed up slow Icinga 2 starts and reloads: jemalloc, pruning apply rules, flat objects, simple assign where filters, Concurrency."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/15-troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting: slow start and reload
Measure first with `time icinga2 daemon -C`.

**Allocator:** install a libjemalloc package (EPEL first on RHEL), find its path with `ldconfig -p | grep libjemalloc`, compare `time env LD_PRELOAD=/path/to/libjemalloc.so.2 icinga2 daemon -C`. If faster, persist via `systemctl edit icinga2.service` with `[Service]` and `Environment=LD_PRELOAD=/path/to/libjemalloc.so.2`; verify with `lsof` on the PID.

**Apply rules and group assignments:**
- `daemon -C` warns `Apply rule ... does not match anywhere!`; remove or comment out such rules, or drop the `assign where` line of unused groups.
- Replace a single-host apply rule (`assign where host.name == "firewall"`) with a plain `object Service` using `host_name`; similarly set `groups` on the host. The docs say v2.13.6+ optimises the apply case, but not group assign conditions.
- Keep `assign where` simple: prefer one custom variable check such as `host.vars.db`; prefer `==` over `match()`.
- Order `&&` operands so a mismatch ends the chain early: `host.vars.production && match("MySQL*", host.name)`.

**Threads:** Icinga starts one thread per CPU core. On systems with more than eight cores fewer can be faster. Benchmark `icinga2 daemon -C -DConfiguration.Concurrency=8` (then 10, 12 and so on), pick the best, and persist it in the systemd `ExecStart=` line.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/15-troubleshooting/. No commands were run.
