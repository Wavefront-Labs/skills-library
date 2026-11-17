---
id: computing-software.networking-hardware-and-wireless.check-point.logging-and-smartlog
name: logging-and-smartlog
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, logging, smartlog, log-server]
level: practitioner
status: draft
description: "Configure Check Point log servers, rule tracking and query logs with filters in SmartConsole Logs & Monitor."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_LoggingAndMonitoring_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SecurityManagement_AdminGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Logging, log servers and SmartLog queries

- Rule **Track** column: None, Log, Detailed Log, Extended Log (Log is default). Accounting adds byte counters, and Alert triggers actions. Logs go to the gateway's log servers (Gateway object > Logs, "Send logs to") and the management server by default.
```
cpstat mg -f log_server
fw log -n -t $FWDIR/log/fw.log | head
fw log -f -n -t fw.log               # follow
fw lslogs                            # list log files, sizes
fw logswitch                         # rotate now
```
- Dedicated Log Server: add a **Check Point Host** with the *Logging & Status* blade and *SIC*, then point gateways at it. Add a Secondary server for resilience.
- Queries in SmartConsole: `src:10.1.10.5 AND action:Drop AND service:443`, `blade:"Application Control"`, `rule_uid:` ... Time ranges and pre-built views; pin useful queries; export to CSV or syslog.
- Retention: logs are indexed; when disk (/var/log) hits the limits ("Log Server > Log Settings > Disk space") the server stops logging at a free-space threshold. Set rotation by size/time and old log deletion.
- Reduce load: avoid Extended Log on high-volume rules, log only drops for noisy allow rules, and disable "Log implied rules".
- Gotcha: a gateway without a reachable log server writes logs locally and shows "Logs: local" in the status; this fills disk. Check `fw ctl pstat` and connectivity (TCP 257).

Verify: generate a connection; `fw log -n -t | tail` locally and SmartConsole shows the entry in under a minute; `cpstat fw -f log` reports "connected" for the log server.
