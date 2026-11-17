---
id: computing-software.systems-network-administration.zabbix.housekeeping-and-queue
name: housekeeping-and-queue
category: computing-software
field: systems-network-administration
product: zabbix
tags: [housekeeping, queue, history-trends, delayed-items, data-retention, retention]
level: practitioner
status: docs-checked
description: "Control data retention with the housekeeper and diagnose delayed items with the queue views."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/web_interface/frontend_sections/administration/housekeeping
  - https://www.zabbix.com/documentation/current/en/manual/web_interface/frontend_sections/administration/queue
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Housekeeping (Administration > Housekeeping) removes outdated data so the database does not grow without bound. It is enabled by default and covers events and alerts (set separately for triggers, services, internal data, discovery and autoregistration), services, user sessions, and history and trends. Audit log housekeeping is configured separately.

Notes:
- Data storage period range is 1 day (1 hour for history) to 25 years, or 0, with time suffixes.
- Only events not tied to unresolved problems are removed. Problems go first, then events.
- History and trends periods also decide how long data shows in Latest data, even with internal housekeeping off.
- Override item history period and Override item trend period replace per-item settings (except Do not store), and work with an external housekeeper too.
- With TimescaleDB, tick both override options and internal housekeeping for history and trends so the housekeeper drops old partitions. Otherwise data is still partitioned, outdated partitions are not dropped and warnings appear.

The queue (Administration > Queue) lists items waiting to be updated. Ideally it is all green. Pages: overview by item type, overview by proxy (server last) and details of delayed items. Columns count items waiting 5-10 s, 10-30 s, 30-60 s, 1-5 min, 5-10 min and over 10 min. A few delayed items are not alarming; many or long delays indicate a performance problem. It works only while the server runs.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (web_interface/frontend_sections/administration/housekeeping; web_interface/frontend_sections/administration/queue): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
