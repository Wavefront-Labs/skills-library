---
id: computing-software.networking-hardware-and-wireless.asterisk.logging-configuration-and-commands
name: logging-configuration-and-commands
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, logging, logger-conf, logfiles, verbose, debug, rotatestrategy, logger-add-channel, queue-log]
level: practitioner
status: docs-checked
description: "Configure logger.conf general and logfiles sections (dateformat, rotatestrategy, levels), use core set verbose/debug and logger commands, and collect debug logs."
sources:
  - https://docs.asterisk.org/Configuration/Core-Configuration/Logging-Configuration/
  - https://docs.asterisk.org/Operation/Logging/Basic-Logging-Commands/
  - https://docs.asterisk.org/Operation/Logging/Collecting-Debug-Information/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# logging configuration and commands
`logger.conf` has `[general]` and `[logfiles]`.

`[general]` options shown: `dateformat` (strftime formats; `%3q` adds milliseconds), `use_callids` (default yes), `appendhostname` (default no), `queue_log` (default yes), `queue_log_to_file`, `queue_log_name`, `queue_log_realtime_use_gmt`, `rotatestrategy` (`none`, `sequential` (default), `rotate`, `timestamp`) and `exec_after_rotate`. With `none`, arrange external rotation: logs grow quickly.

`[logfiles]`: `filename => level,level`. Names are relative to `astlogdir` or absolute. `syslog` and `console` are reserved. Levels: `debug`, `notice`, `warning`, `error`, `dtmf`, `fax`, `security`, `verbose(<level>)`, or `*` for all including dynamic levels. Do not leave `debug` on in production.
```
console => notice,warning,error
security => security
full => notice,warning,error,verbose,dtmf,fax
```
CLI: `core set verbose [atleast] <level> [silent]`, `core set debug [atleast] <level> [module]` (0 or off disables), `logger show channels`, `logger rotate`, `logger reload`, `core show settings`.

For an issue report, add a dedicated file, for example `debug_log_123456 => notice,warning,error,debug,verbose,dtmf`, or at the CLI `logger add channel <name> <levels>` (lasts until restart, logger reload or rotation); then raise verbose and debug to 5 and reload the logger module.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Logging-Configuration, Basic-Logging-Commands, Collecting-Debug-Information) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
