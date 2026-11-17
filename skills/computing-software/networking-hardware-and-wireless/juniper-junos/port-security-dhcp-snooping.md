---
id: computing-software.networking-hardware-and-wireless.juniper-junos.port-security-dhcp-snooping
name: port-security-dhcp-snooping
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, dhcp-snooping, port-security, arp-inspection, storm-control]
level: practitioner
status: draft
description: "Enable DHCP snooping, dynamic ARP inspection, MAC limiting and storm control on access ports."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Layer 2 security on EX/QFX
Goal: reduce rogue DHCP, ARP spoofing and broadcast storms.

```
set vlans USERS forwarding-options dhcp-security ip-source-guard
set vlans USERS forwarding-options dhcp-security arp-inspection
set vlans USERS forwarding-options dhcp-security group TRUST overrides trusted
set vlans USERS forwarding-options dhcp-security group TRUST interface xe-0/0/47
set ethernet-switching-options secure-access-port interface ge-0/0/10 mac-limit 3 action drop
set forwarding-options storm-control-profiles SC all bandwidth-percentage 5
set interfaces ge-0/0/10 unit 0 family ethernet-switching storm-control SC
```

```
user@host> show dhcp-security binding
user@host> show dhcp-security arp inspection statistics
```

- Mark uplinks and DHCP server ports as trusted; access ports untrusted.
- Syntax differs between ELS and older EX releases: confirm.

Gotcha: enabling snooping with the uplink not trusted blocks every DHCP offer. Leave bindings database persistence in mind after reboot.

Operational tip: roll out in monitor mode where possible, confirm that static-IP hosts have entries, and keep the trusted-port list in change control since it is the main failure source.

## Verify
- `show dhcp-security binding` lists client leases; a rogue DHCP server on an access port is dropped.
