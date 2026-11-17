---
id: computing-software.systems-network-administration.nagios-core.fast-startup-precache
name: fast-startup-precache
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, fast-startup, precached-object-file, precache, nagios-pv, skip-circular-check, startup-time]
level: advanced
status: docs-checked
description: "Cut Nagios Core startup time with a precached object file (-p with -v), starting with -u, and skipping circular path checks with -x, including the stale-cache trap."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/faststartup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fast startup

Measure first: `nagios -s nagios.cfg` prints per-stage timings and estimated savings. (Docs example: 25 hosts, ~10,000 services, 68 s startup, about 5 s possible.) Since Core 4 manual optimisation matters less.

## Precache (-p)
`nagios -pv nagios.cfg` verifies then writes the cache to `precached_object_file`. `-p` must be paired with `-v` or `-s`. Start from the cache with `-u`: `nagios -ud nagios.cfg`.

## Skip circular path checks (-x)
The slowest verification step, detecting loops in host, host dependency and service dependency definitions. `nagios -xd nagios.cfg`. Verify first or circular dependencies can deadlock Nagios logic.

## Procedure
1. `nagios -vp nagios.cfg`
2. Stop Nagios.
3. `nagios -uxd nagios.cfg`
4. After editing config, repeat step 1, then restart (web UI or SIGHUP).

## Trap
Any source config change needs re-verify and re-cache; otherwise Nagios keeps running the old cached config.

See also `computing-software.systems-network-administration.nagios-core.verify-configuration`.

## Checked

2026-11-04. Confirmed against the Fast Startup page: -s timing output and the 25 hosts / just over 10,000 services / about 68 seconds to 5 seconds example, -p paired with -v or -s, -u to use the precached file, -x skipping circular path checks with the deadlock warning, the four-step procedure and the re-verify and re-cache requirement.

Method: documentation only; no commands were run.
