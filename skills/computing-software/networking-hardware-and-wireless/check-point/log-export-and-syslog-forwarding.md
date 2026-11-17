---
id: computing-software.networking-hardware-and-wireless.check-point.log-export-and-syslog-forwarding
name: log-export-and-syslog-forwarding
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, log-exporter, cp-log-export, siem-forwarding]
level: practitioner
status: draft
description: "Use Check Point Log Exporter (cp_log_export) to forward logs to a SIEM via syslog with TLS, format and filters."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_LoggingAndMonitoring_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Log Exporter and syslog forwarding to SIEM

```
cp_log_export add name siem1 target-server 10.9.9.60 target-port 6514 protocol tcp format cef
cp_log_export set name siem1 protocol tcp encrypted true ca-cert /var/tmp/ca.pem
cp_log_export restart name siem1
cp_log_export show
cp_log_export status name siem1
cp_log_export delete name siem1
```
- Log Exporter runs on the management or log server, reading the live log stream, not exported files. Formats: `syslog`, `cef`, `leef`, `json`, `generic` (key=value); use the one your SIEM's connector parses.
- Transport: UDP, TCP, or TLS-encrypted TCP with a CA certificate (and client certificate for mutual TLS: `client-cert` parameter, confirm). Use TCP/TLS to avoid loss and eavesdropping.
- Filters: a `filter.conf` (in the exporter directory under `$EXPORTERDIR/targets/<name>/conf`) can select by blade or field to cut volume. Use `cp_log_export set ... ` options or edit then `restart`.
- Gotcha: after upgrades, re-add or verify targets with `cp_log_export show`; a stopped exporter does not backfill missed logs (it resumes at the current position by default; `--read-mode` options, confirm).
- On Multi-Domain servers, add the exporter per Domain Log Server.

Verify: `cp_log_export status` shows `running`; on the SIEM host, `tcpdump -nni any port 6514` shows traffic and a sample parsed event with `product=` and `action=` fields.
