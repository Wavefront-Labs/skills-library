---
id: computing-software.networking-hardware-and-wireless.juniper-junos.syslog
name: syslog
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, syslog, system-log, log-files, logging]
level: practitioner
status: draft
description: "Configure Junos syslog to files and remote servers with facility/severity, and read messages with show log."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# System logging (syslog)
Goal: capture useful logs locally and forward them off-box.

```
set system syslog file messages any notice
set system syslog file messages authorization info
set system syslog file interactive-commands interactive-commands any
set system syslog host 192.0.2.60 any warning
set system syslog host 192.0.2.60 port 514
set system syslog source-address 10.255.0.1
```

```
user@host> show log messages | last 50
user@host> show log messages | match "UI_COMMIT|RPD_OSPF"
user@host> monitor start messages
user@host> monitor stop
```

- `interactive-commands` records every CLI command by user.
- `archive size 10m files 5` rotates log files; `file X match "regex"` filters.
- `UI_COMMIT` and `UI_LOGIN_EVENT` messages are the change/audit trail.

Gotcha: using `any any` on a busy router floods flash and the remote collector; use `any notice` for files. Remote syslog over UDP is unacknowledged, so verify arrival at the collector, not just config.

## Verify
- Make a commit and see `UI_COMMIT_COMPLETED` in `show log messages` and on the collector.
