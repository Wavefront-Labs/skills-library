---
id: computing-software.networking-hardware-and-wireless.juniper-junos.snmp
name: snmp
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, snmp, snmpv3, community, traps]
level: practitioner
status: draft
description: "Configure Junos SNMPv2c communities with client lists and SNMPv3 users, traps and contact info."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SNMP configuration
Goal: allow monitoring polls from the NMS only.

```
set snmp location "DC1 rack 12"
set snmp contact noc@example.net
set snmp community poll-ro authorization read-only
set snmp community poll-ro clients 192.0.2.60/32
set snmp community poll-ro clients 0.0.0.0/0 restrict
set snmp trap-group nms targets 192.0.2.60
set snmp v3 usm local-engine user monitor authentication-sha authentication-password "<redacted>"
set snmp v3 usm local-engine user monitor privacy-aes128 privacy-password "<redacted>"
```

- Prefer SNMPv3 with auth and privacy; v2c communities are clear text.
- `routing-instance-access` is needed to poll within a routing instance.
- `set snmp interface fxp0.0` limits which interfaces answer SNMP.

Gotcha: a community without `clients` answers everyone who can reach it; always bound it and add a loopback filter permitting UDP 161 only from the NMS.

Operational tip: after changing communities, rotate them on the NMS in the same window and remove the old community; also review `show snmp mib walk system` output for sensitive location or contact strings.

## Verify
- `show snmp statistics` counters grow on poll.
- From the NMS: `snmpwalk -v3 -u monitor -l authPriv <device> sysName` returns the hostname.
