---
id: computing-software.networking-hardware-and-wireless.juniper-junos.re-protection-filter
name: re-protection-filter
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, loopback-filter, re-protection, lo0-filter, control-plane-policing]
level: practitioner
status: draft
description: "Protect the Junos routing engine with an lo0.0 filter permitting only management and routing traffic."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Routing-engine protection with a loopback filter
Goal: stop unsolicited traffic from reaching the control plane.

```
set policy-options prefix-list MGMT-NETS 192.0.2.0/24
set firewall family inet filter PROTECT-RE term ssh from source-prefix-list MGMT-NETS
set firewall family inet filter PROTECT-RE term ssh from protocol tcp
set firewall family inet filter PROTECT-RE term ssh from destination-port [ ssh 830 ]
set firewall family inet filter PROTECT-RE term ssh then accept
set firewall family inet filter PROTECT-RE term routing from protocol [ ospf bgp ]
set firewall family inet filter PROTECT-RE term routing then accept
set firewall family inet filter PROTECT-RE term icmp from protocol icmp
set firewall family inet filter PROTECT-RE term icmp then policer ICMP-LIMIT
set firewall family inet filter PROTECT-RE term icmp then accept
set firewall family inet filter PROTECT-RE term default then discard
set interfaces lo0 unit 0 family inet filter input PROTECT-RE
```

- It applies to traffic destined to any address on the device, from any interface.
- Include NTP, SNMP, DNS replies, BFD, VRRP and traceroute as needed.

Gotcha: a missing allow term for a routing protocol drops it only after the next hello timeout, so a lockout or flap can look delayed. Always `commit confirmed 5`.

## Verify
- `show firewall filter PROTECT-RE` shows hit counters; `show ospf neighbor` and BGP stay up after commit.
