---
id: computing-software.networking-hardware-and-wireless.juniper-junos.firewall-filters
name: firewall-filters
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, firewall-filters, stateless-filter, policer, family-inet-filter]
level: practitioner
status: draft
description: "Write Junos firewall filters with terms, match conditions, actions and counters, and apply them inbound/outbound."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stateless firewall filters
Goal: permit/deny/count packets on interfaces.

```
set firewall family inet filter EDGE-IN term allow-ssh from source-prefix-list MGMT-NETS
set firewall family inet filter EDGE-IN term allow-ssh from protocol tcp
set firewall family inet filter EDGE-IN term allow-ssh from destination-port ssh
set firewall family inet filter EDGE-IN term allow-ssh then count ssh-in
set firewall family inet filter EDGE-IN term allow-ssh then accept
set firewall family inet filter EDGE-IN term default then count dropped
set firewall family inet filter EDGE-IN term default then discard
set interfaces xe-0/0/3 unit 0 family inet filter input EDGE-IN
```

- There is an implicit discard at the end of every filter; add `accept` terms deliberately.
- Actions: accept, discard, reject, count, log, syslog, policer, next term, forwarding-class, routing-instance.
- Use `commit confirmed` when applying a filter to a remote interface.

Gotcha: a filter on a transit interface does not protect the routing engine; for that use a `lo0` filter. Terms with only `then count` do not terminate; add `next term` or an explicit action.

## Verify
- `show firewall filter EDGE-IN` counters increment; `show firewall log` shows logged packets.
