---
id: computing-software.networking-hardware-and-wireless.kea.keactrl-service-control
name: keactrl-service-control
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, keactrl, keactrl-conf, pid-file, service-control]
level: intro
status: docs-checked
description: "Start, stop, reload and check Kea servers with keactrl: commands, keactrl.conf variables, the -s and -c switches, and the systemd note."
sources:
  - https://kea.readthedocs.io/en/latest/arm/keactrl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# keactrl service control
Commands: `start`, `stop`, `reload` (sends SIGHUP), `status`, `version`.

Configuration is `keactrl.conf`, by default at `[kea-install-dir]/etc/kea/keactrl.conf`; override with `-c`. Variables: `dhcp4`, `dhcp6`, `dhcp_ddns`, `netconf` (each yes or no) and `kea_verbose`.

```
keactrl start -s dhcp4
```

The `-s` switch takes one or more of the keywords dhcp4, dhcp6, dhcp_ddns, netconf. On start and reload, servers not enabled in keactrl.conf are ignored; on stop, no such check is made.

keactrl uses PID files to detect running servers.

Native packages use systemd instead of keactrl, and the docs recommend systemctl where available.

## Checked

2026-11-08. Read the keactrl chapter in full: commands, SIGHUP on reload, keactrl.conf default path and variables, the -c and -s switches and keywords, start versus stop enabled-server checks, PID files and the systemd recommendation. All claims confirmed; nothing removed.

Method: documentation only; no commands were run.
