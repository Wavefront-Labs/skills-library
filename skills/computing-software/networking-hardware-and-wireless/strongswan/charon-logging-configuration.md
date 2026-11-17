---
id: computing-software.networking-hardware-and-wireless.strongswan.charon-logging-configuration
name: charon-logging-configuration
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, logging, filelog, syslog, log-levels, subsystems]
level: practitioner
status: docs-checked
description: "Configure charon logging: levels -1 to 4, subsystem names, filelog and syslog loggers in strongswan.conf, JSON and timestamp options, and reload via SIGHUP."
sources:
  - https://docs.strongswan.org/docs/latest/config/logging.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# charon logging configuration
By default charon logs through syslog(3): `LOG_AUTHPRIV` (level 0 only) and `LOG_DAEMON` (all levels), default level 1 for every subsystem. `charon-systemd` logs to the journal instead and has its own logger section.

**Levels:** -1 silent, 0 basic auditing (SA up/down), 1 control flow and errors (good default), 2 more detailed debugging, 3 raw hex dumps, 4 also sensitive material such as keys.

**Subsystems:** `app asn cfg chd dmn enc esp ike imc imv job knl lib mgr net pts tls tnc` (and `wch` for the file descriptor watcher).

**File loggers** go under `charon.filelog`; `<name>` is an absolute path, `stdout`, `stderr`, or any name if `path` is set (section names cannot contain dots or colons). Keys: `path`, `default` (1), `<subsystem>` level, `append` (yes), `flush_line` (no), `ike_name` (no, adds connection name and IKE_SA id), `json` (no), `log_level` (no), `time_format` (strftime), `time_precision` (`ms` or `us`).

**Syslog loggers** go under `charon.syslog`: `identifier`, and per facility `<facility>.default`, `<facility>.<subsystem>`, `<facility>.ike_name`.

```
charon {
  filelog {
    charon { path = /path/to/charon.log
             default = 1
             ike = 2 }
  }
}
```

SIGHUP, or `swanctl --reload-settings`, reloads the loggers, which lets you rotate log files without restarting.

## Checked
2026-11-04. Confirmed against the strongSwan Logging page: default facilities and level, levels -1 to 4, the subsystem list, filelog and syslog keys and defaults, section-name restrictions, and reload behaviour.

Method: documentation only; no commands were run.
