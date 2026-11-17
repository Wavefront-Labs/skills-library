---
id: computing-software.cybersecurity-defensive.network-defence.firewall-policy-analysis
name: firewall-policy-analysis
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [firewall-policy-analysis, rule-base-analysis, shadowed-rules, tufin, algosec, firemon, capirca, batfish]
level: advanced
status: draft
description: "Analyse firewall rule bases with tools: shadowed/redundant/overly permissive rules, path analysis, compliance checks, risk scoring and simulating changes before deployment."
sources: ["https://batfish.readthedocs.io/en/latest/", "https://www.algosec.com/", "https://www.tufin.com/", "https://github.com/google/capirca"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Firewall policy analysis tools

## What analysis finds
- **Shadowed rules:** never matched because an earlier rule covers them fully.
- **Redundant rules:** duplicate coverage; safe to merge.
- **Overly permissive:** any/any, large ranges, all ports, broad internet inbound.
- **Unused:** zero hits over 90+ days (from device hit counters/logs).
- **Compliance violations:** rules permitting traffic forbidden by zone policy (e.g. internet -> PCI, clear-text to OT).
- **Path questions:** "can host A reach B on 445?" across multiple firewalls and routers.

## Tools
| Tool | Strength |
|---|---|
| Tufin, AlgoSec, FireMon, Skybox | Commercial multi-vendor: cleanup reports, change workflow, risk analysis, topology path queries |
| Batfish (open source) | Offline config analysis: reachability queries, ACL/filter line reachability (shadowing), what-if on proposed changes |
| Capirca (open source) | Write policy once, generate vendor configs - prevents drift by design |
| Vendor native | PAN-OS Policy Optimizer (unused apps/ports), FortiManager policy analysis, Azure Firewall Policy Analytics |

## Batfish example
```python
from pybatfish.client.session import Session
bf = Session(host="localhost"); bf.set_network("dc"); bf.init_snapshot("configs/", name="base")
bf.q.filterLineReachability().answer().frame()        # unreachable (shadowed) lines
bf.q.reachability(pathConstraints=PathConstraints(startLocation="@enter(fw1[outside])"),
                  headers=HeaderConstraints(dstIps="10.20.0.0/16", applications=["rdp"])).answer()
```

## Process
Monthly: run cleanup report, owners confirm removals, disable first, delete after 30 days. Before each
change: run what-if (Batfish/commercial simulation) against compliance rules.

## Gotchas
- Hit counters reset on reboot/upgrade on some platforms; use log data for unused-rule decisions.
- Analysis on stale config exports misleads; pull configs automatically.

## Verify
- [ ] Monthly report trend: shadowed/unused/permissive counts falling.
- [ ] Compliance checks gate changes.
