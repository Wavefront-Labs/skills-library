---
id: computing-software.systems-network-administration.zabbix.log-monitoring-items
name: log-monitoring-items
category: computing-software
field: systems-network-administration
product: zabbix
tags: [log-monitoring, logrt, log-count, active-agent, log-time-format, log, monitoring]
level: practitioner
status: docs-checked
description: "Monitor log files with active log[] and logrt[] items, including permissions, rotation tracking and time format."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/zabbix_agent/log_items
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Log items are active checks, so the agent needs ServerActive set and a Hostname that matches the frontend host.

Item setup:
- Type: Zabbix agent (active).
- Key: log[] or logrt[] to monitor lines matching a regexp, for example log[/var/log/syslog,error]. logrt[] handles rotated files. log.count[] and logrt.count[] return the count of matched lines instead.
- The file must be readable by the zabbix user, otherwise the item turns unsupported.
- Type of information is filled in automatically: Log for log[] and logrt[], Numeric (unsigned) for the count keys. With the output parameter you can choose another type, which stores no log metadata.
- Update interval controls how often the agent looks for new lines; 1 second gives the quickest delivery.
- Log time format optionally parses a timestamp in each line with placeholders y, M, d, h, m, s. If blank the timestamp is 0 (1 January 1970).

How tracking works: server and agent keep counters for log size and, for logrt, last modification time. The agent also uses inode numbers on UNIX (file indexes on Windows NTFS, file IDs on ReFS) and MD5 sums of the first 512 bytes to decide what to do when files are truncated or rotated. Where file indexes change, as on FAT32 and exFAT, a fall-back algorithm is used.

If a log item is added while its host is in a no-data maintenance, only entries written after the maintenance ends are collected.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (config/items/itemtypes/zabbix_agent/log_items): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
