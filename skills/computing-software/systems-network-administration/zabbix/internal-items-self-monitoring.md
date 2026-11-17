---
id: computing-software.systems-network-administration.zabbix.internal-items-self-monitoring
name: internal-items-self-monitoring
category: computing-software
field: systems-network-administration
product: zabbix
tags: [internal-items, zabbix-process, self-monitoring, wcache, queue, internal, zabbix, process]
level: advanced
status: docs-checked
description: "Watch Zabbix's own health with zabbix[] internal items such as process busy percentage, caches and queue."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/internal
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Internal items report on Zabbix itself and use item type Zabbix internal. The central key is zabbix[process,<type>,<mode>,<state>].

- type is a process name such as poller, trapper, "history syncer" or "icmp pinger" (quote names with spaces).
- mode is avg (default), count, max, min, or a process number from 1 to the number of forks. A number for a process that is not running makes the item unsupported.
- state is busy (default) or idle. The value is a percentage of the last minute.

Examples: zabbix[process,poller,avg,busy], zabbix[process,"icmp pinger",max,busy], zabbix[process,trapper,count]. Min and max refer to a single process. Processes record their state in shared memory and a self-monitoring process summarises it each second; a state change is recorded on change, so a hung process correctly reads as 100% busy. Asynchronous pollers count as busy when they reach MaxConcurrentChecksPerPoller.

Other useful keys: zabbix[wcache,history,pused] (history write cache usage, which also shows proxy throttling), zabbix[rcache,...] (configuration cache), zabbix[vcache,...] (value cache), zabbix[queue,...], zabbix[requiredperformance], zabbix[uptime], zabbix[discovery_queue], and zabbix[proxy,<name>,lastaccess]. Some keys are not supported on server or on proxy; the docs mark which.

Alert on sustained high busy percentages and high cache usage, then raise the matching Start* process count or cache size.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (config/items/itemtypes/internal): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
