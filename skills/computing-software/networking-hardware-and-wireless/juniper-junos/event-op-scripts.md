---
id: computing-software.networking-hardware-and-wireless.juniper-junos.event-op-scripts
name: event-op-scripts
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, event-options, op-scripts, event-policy, commit-scripts]
level: practitioner
status: draft
description: "Automate on-box with Junos event policies, op scripts and commit scripts."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Event policies and op/commit scripts
Goal: react to events on the device.

```
set event-options policy LINKDOWN events SNMP_TRAP_LINK_DOWN
set event-options policy LINKDOWN then execute-commands commands "show interfaces terse"
set event-options policy LINKDOWN then execute-commands output-filename linkdown.txt destination local-file
set event-options destinations local-file archive-sites /var/tmp
set system scripts op file check-bgp.slax
set system scripts language python3
```

```
user@host> op check-bgp
user@host> show event-options event-scripts policies
```

- Op scripts run on demand, commit scripts run at commit and can reject or change a config, event scripts run on a policy match.
- Languages: SLAX, XSLT and Python 3 on newer releases (confirm on your platform); scripts are copied to `/var/db/scripts/op`.
- Use `commit-script` checks to enforce standards.

Gotcha: scripts run with the login-class of the user (or `jcs:` with `system scripts ... allow-url`). A buggy commit script can block all commits; keep it in a `rollback rescue` safe setup.

## Verify
- `op check-bgp` returns output, and the event policy log appears in `show log messages`.
