---
id: computing-software.networking-hardware-and-wireless.powerdns.pdns-control-zones-and-stats
name: pdns-control-zones-and-stats
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, pdns-control, list-zones, notify, retrieve, statistics, qtypes, respsizes]
level: practitioner
status: docs-checked
description: "pdns_control zone and statistics commands: list-zones, notify, notify-host, retrieve, list, show, remotes, respsizes, qtypes, uptime."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/manpages/pdns_control.1.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pdns_control zone and statistics commands

Zones:
- `list-zones [primary|secondary|native]`: list zones, optionally by kind.
- `notify <ZONE>`: queue notifications to the zone's nameservers; `*` means all zones.
- `notify-host <ZONE> <ADDRESS>`: notify one specific address.
- `retrieve <ZONE> [IP]`: pull a secondary zone from its primary now; with an IP the transfer is forced from that address.

Statistics:
- `list`: all statistics comma-separated, same as `show *`.
- `show <STATISTIC>`: one statistic; a single trailing `*` matches a prefix.
- `status`: usage statistics (guardian mode only).
- `remotes`: most frequent client addresses.
- `respsizes`: histogram of response sizes.
- `qtypes`: query counts per qtype.
- `uptime`: how long the server has run.

BIND backend commands (`bind-add-zone`, `bind-domain-status`, `bind-list-rejects`, `bind-reload-now`) are covered in the bind backend skill; `bind-add-zone` needs an absolute path and does not write the BIND config.

## Checked

2026-11-08. Read in full: PowerDNS docs manpages/pdns_control.1.rst. Confirmed list-zones, notify (including the star for all zones), notify-host, retrieve with optional IP, and the statistics commands list, show, status, remotes, respsizes, qtypes and uptime, plus the bind-add-zone absolute-path note. Nothing removed.

Method: documentation only; no commands were run.
