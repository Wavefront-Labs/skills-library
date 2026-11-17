---
id: computing-software.systems-network-administration.zabbix.sizing-and-requirements
name: sizing-and-requirements
category: computing-software
field: systems-network-administration
product: zabbix
tags: [sizing, requirements, database, disk-space]
level: intro
status: docs-checked
description: "Size a Zabbix server from metric count, estimate database disk growth, and pick supported databases and ports."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/installation/requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start from the docs' sizing table, then benchmark in staging. One metric is roughly one item plus one trigger plus one graph. Examples given: small 1 000 metrics (2 cores, 8 GiB), medium 10 000 (4 cores, 16 GiB), large 100 000 (16 cores, 64 GiB), very large 1 000 000 (32 cores, 96 GiB). Run the database on a separate server for large installations.

Supported backends are MySQL or Percona 8.0.30 and later (InnoDB required), MariaDB 10.5 and later, and PostgreSQL 13 and later. For PostgreSQL you may need to raise work_mem (default 4MB).

Estimate disk with these rules:
- Values per second = items / refresh rate. 3000 items at 60 s is 50 values per second.
- History: about 90 bytes per numeric value. 30 days at 50 values per second is about 130 million values, roughly 10.9 GB. Text and log values are around 500 bytes.
- Trends: one record per item per hour, about 90 bytes each.
- Events: about 250 bytes, plus about 80 for the recovery record and about 100 per tag.
- Total = configuration (about 10 MB) + history + trends + events.

Disk use grows until the housekeeper settings cap it, not immediately after install. Keep system clocks synchronised on every Zabbix host. Open only the ports each component needs (agent 10050 only from the server or proxy) and never expose Zabbix ports to the internet.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (installation/requirements): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
