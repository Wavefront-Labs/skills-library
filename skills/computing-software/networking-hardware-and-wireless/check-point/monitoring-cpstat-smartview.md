---
id: computing-software.networking-hardware-and-wireless.check-point.monitoring-cpstat-smartview
name: monitoring-cpstat-smartview
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, cpstat, smartview-monitor, snmp-monitoring]
level: practitioner
status: draft
description: "Check gateway health with cpstat, SmartView Monitor views and SNMP (Gaia UDP 161) for CPU, memory, connections and tunnels."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_LoggingAndMonitoring_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_Gaia_AdminGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Monitoring with cpstat, SmartView and SNMP

```
cpstat os -f cpu
cpstat os -f memory
cpstat os -f perf
cpstat fw -f policy
cpstat fw -f sync
cpstat vpn -f tunnels
cpstat ha -f all
```
- `cpstat <app> -f <flavour>` queries the same data SmartConsole shows; `cpstat -h` lists applications. It is the right tool for scripts and for validating a check without GUI.
- **SmartView Monitor**: Logs & Monitor > open **Gateway Status**, **Tunnels**, **Traffic** and **Cooperative Enforcement** views; thresholds alert via mail/script (Gateway object > Logs > Alert Commands).
- SNMP on Gaia: enable in the WebUI (System Management > SNMP) or clish:
```
set snmp agent on
set snmp community public read-only
set snmp traps receiver 10.9.9.50 version v2 community public
set snmp mode v3-Only
add snmp usm user monitor security-level authPriv auth-pass-phrase "..." privacy-pass-phrase "..."
save config
```
- Gaia SNMP serves OS MIBs and Check Point MIB (`.1.3.6.1.4.1.2620`). Restrict via `set snmp ... allowed` or firewall rules, and use v3 where possible; public communities in plain UDP are insecure.
- Gotcha: the SNMP service responds only on interfaces allowed by Gaia's Network Access settings; the gateway's own policy implied rules must also accept SNMP (implied rules are on by default).

Verify: `snmpwalk -v3 -u monitor -l authPriv ... <gw> .1.3.6.1.4.1.2620.1.1` returns `fwModuleState`; `cpstat os -f cpu` matches `top`.
