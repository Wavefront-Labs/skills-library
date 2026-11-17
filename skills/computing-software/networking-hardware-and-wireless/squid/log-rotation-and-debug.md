---
id: computing-software.networking-hardware-and-wireless.squid.log-rotation-and-debug
name: log-rotation-and-debug
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, logfile-rotate, debug-options, cache-log, squid-k-rotate]
level: practitioner
status: docs-checked
description: "Rotate logs with logfile_rotate and squid -k rotate, and control cache.log verbosity with debug_options."
sources:
  - https://www.squid-cache.org/Doc/config/logfile_rotate/
  - https://www.squid-cache.org/Doc/config/debug_options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log rotation and debug levels
`logfile_rotate` (default 10) is the number of rotations done by `squid -k rotate`, extensions 0 to 9. 0 disables renaming, but logs are still closed and reopened so you can rename them yourself. Use `squid -k rotate` rather than a manual USR1. From Squid 3.1 it defaults only cache.log; from Squid 4 it applies to access.log written by the stdio module, which can use `rotate=N` on `access_log`.

`debug_options` sets `section,level` pairs; default `ALL,1`. Level 9 can create a very large log. Its `rotate=N` option overrides how many cache.log files are kept.

## Checked

2026-11-04. Read the logfile_rotate and debug_options directive pages and confirmed the default of 10, extensions 0 to 9, the 0 setting, the Squid 3.1 and 4 scope notes, the USR1 advice, ALL,1, level 9 warning and rotate=N. Nothing was removed.

Method: documentation only; no commands were run.
