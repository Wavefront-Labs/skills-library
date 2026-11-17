---
id: computing-software.networking-hardware-and-wireless.check-point.connection-table-fw-tab
name: connection-table-fw-tab
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, fw-tab, connection-table, kernel-tables]
level: practitioner
status: draft
description: "Inspect and size the Check Point kernel connection table with fw tab, find a connection and spot table exhaustion."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_PerformanceTuning_AdminGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Connection table inspection with fw tab

```
fw tab -t connections -s                      # summary: entries (#VALS), peak (#PEAK), limit
fw tab -t connections -f | grep 10.1.10.55    # formatted dump, filter
fw tab -t connections -u | head               # unformatted
fw tab -t sam_requests -s
fw ctl pstat                                   # memory, connection counts, sync
fw tab -t connections -x                       # delete all entries (disruptive!)
```
- `-s` shows `NAME`, `ID`, `#VALS`, `#PEAK`, `#SLINKS`. When `#PEAK` approaches the table limit (set in the gateway object > Optimizations > Maximum concurrent connections, or `fwkern.conf`), new connections drop with "Connection table limit reached"/`F2F` log messages.
- Connection entries are hex-encoded addresses `<dir,srcIP,srcPort,dstIP,dstPort,proto>`; `-f` decodes them. Entries stay until idle timeout (TCP 3600 s default established, 60 s for half-open `SYN`; service-specific timeouts in the service object > Advanced).
- Do not run `-x` or `fw tab -t connections -d` in production unless intended; use `fw tab -t connections -x -e <entry>` for a single deletion (confirm syntax).
- To raise the limit: gateway properties > Capacity Optimization; memory and the `hash size` auto-adjust (R80.30+). Check `fw ctl pstat` "Hash kernel memory" afterwards.
- Gotcha: long idle timeouts for services like SSH, Oracle or LDAP on firewalls block pooled connections that idle longer than TCP 3600 s; set service timeout or use keepalives.

Verify: `fw tab -t connections -s` shows `#VALS` below the limit; after changing the limit and installing policy, the new limit appears in the `-s` output.
