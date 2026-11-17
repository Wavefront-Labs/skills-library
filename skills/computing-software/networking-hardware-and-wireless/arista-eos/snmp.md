---
id: computing-software.networking-hardware-and-wireless.arista-eos.snmp
name: snmp
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, snmp, snmpv3, snmp-server, traps]
level: practitioner
status: draft
description: "Configure EOS SNMPv2c/v3, ACL restriction, traps and views."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SNMP
Goal: monitoring access, restricted to the NMS.

```
ip access-list SNMP-ACL
   10 permit ip host 192.0.2.60 any
snmp-server community poll-ro ro SNMP-ACL
snmp-server contact noc@example.net
snmp-server location DC1-row3
snmp-server host 192.0.2.60 version 3 priv monitor
snmp-server user monitor MONGROUP v3 auth sha <placeholder> priv aes <placeholder>
snmp-server enable traps
```

```
show snmp
show snmp community
show snmp user
```

- Prefer SNMPv3 with auth and privacy.
- `snmp-server vrf MGMT` makes SNMP listen in the management VRF (confirm syntax on your release).
- Interface counters use 64-bit counters in the IF-MIB (ifHCInOctets).

Gotcha: SNMP replies through the wrong VRF are dropped; the agent must be bound to the VRF where the NMS lives.

Operational tip: prefer streaming telemetry for high-frequency metrics and keep SNMP for compatibility, traps and inventory. Rate-limit pollers to avoid CPU spikes on large tables like the routing table.

## Verify
- `show snmp` increments counters on poll; `snmpwalk` from the NMS returns sysName.
