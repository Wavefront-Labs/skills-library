---
id: computing-software.networking-hardware-and-wireless.squid.snmp-port
name: snmp-port
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, snmp, snmp-port, monitoring]
level: practitioner
status: docs-checked
description: "Enable the Squid SNMP agent by building with --enable-snmp and setting snmp_port."
sources:
  - https://www.squid-cache.org/Doc/config/snmp_port/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# snmp_port
SNMP is disabled by default (port 0). Squid must be compiled with `--enable-snmp`. Port 3401 is a common choice for the Squid agent.
```
snmp_port 3401
```

## Checked

2026-11-04. Read the snmp_port directive page and confirmed the build option, the disabled default and port 3401. Nothing was removed.

Method: documentation only; no commands were run.
