---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-vlan-interfaces-and-software-switch
name: fortigate-vlan-interfaces-and-software-switch
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [vlan-interface, fortios, 802-1q, software-switch, hardware-switch, switch-interface, trunk]
level: practitioner
status: draft
description: "Create FortiGate 802.1Q VLAN subinterfaces and understand software versus hardware switch interfaces."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: VLAN-tagged networks on a physical trunk port, or bridged ports on small models.

```
config system interface
    edit "vlan100"
        set vdom "root"
        set type vlan
        set vlanid 100
        set interface "port2"
        set ip 10.100.0.1 255.255.255.0
        set allowaccess ping
        set role lan
    next
end
```
Software switch (bridges ports in software; one IP, fine for small sites):
```
config system switch-interface
    edit "lan-sw"
        set vdom "root"
        set member "port3" "port4"
        set type switch
    next
end
config system interface
    edit "lan-sw"
        set ip 10.50.0.1 255.255.255.0
    next
end
```
Hardware switch (`config system virtual-switch`) uses the switch ASIC where the model supports it and offloads better.

Gotchas
- The upstream switch port must be a trunk allowing the VLAN; a mismatch gives link up and no traffic.
- Member ports of a software switch must not carry IPs or be used in policies on their own.
- VLAN IDs are scoped per parent interface; the same ID on a different parent is a different network.

## Verify
```
get system interface
diagnose sniffer packet port2 'vlan 100' 4 10 l
```
The sniffer shows tagged frames; ARP from hosts in VLAN 100 resolves the gateway.
