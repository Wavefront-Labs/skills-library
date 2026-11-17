---
id: computing-software.systems-network-administration.cisco-networking.ios-arp-table-troubleshooting
name: ios-arp-table-troubleshooting
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, arp, incomplete-arp, show-ip-arp, proxy-arp, arp-timeout, gratuitous-arp, glean]
level: practitioner
status: draft
description: "Troubleshoot ARP on IOS: Incomplete entries, proxy ARP surprises, ARP vs MAC aging mismatch, duplicate IPs, and clearing entries safely."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/dynamic-address-allocation-resolution/13718-5.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_arp/configuration/xe-16/arp-xe-16-book.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ARP table troubleshooting on IOS

## Reading the table
```
show ip arp
Protocol  Address      Age (min)  Hardware Addr   Type   Interface
Internet  10.10.0.1           -   0011.2233.4401  ARPA   Vlan10     ! own address ('-')
Internet  10.10.0.20          3   0050.5611.2222  ARPA   Vlan10
Internet  10.10.0.30          0   Incomplete      ARPA
show ip arp summary
show ip arp vrf CUST-A
```

## Incomplete
The router sent ARP requests and got no reply. Causes:
- Host down, wrong VLAN, or host firewall dropping ARP (rare) / wrong subnet mask on host.
- L2 path broken (trunk not allowing the VLAN, STP blocking, DAI dropping replies).
- Scans or traffic to unused addresses: many Incomplete entries, glean punts and CPU load.
Check: `show mac address-table address <mac>` from the switch side, `show interfaces trunk`,
`show ip arp inspection statistics`.

## Proxy ARP
On by default on IOS interfaces (`ip proxy-arp`). The router answers ARP for addresses it can
route to. Hosts with wrong masks or default routes pointing to an interface "work" via proxy ARP,
hiding misconfigurations; and a router can attract traffic it should not.
```
interface Vlan10
 no ip proxy-arp
```
Static routes pointing only to an Ethernet exit interface rely on proxy ARP from the next router.

## ARP timeout vs MAC aging
ARP default 4 hours; switch MAC aging 5 minutes. For a host that only receives, the router still
has its ARP entry but switches have aged the MAC: traffic is flooded (unicast flooding). Align:
`arp timeout 300` on SVIs, or raise MAC aging on that VLAN.

## Duplicate IPs
`%IP-4-DUPADDR: Duplicate address 10.10.0.1 on Vlan10, sourced by 0050.5699.0001`. Find the MAC
with `show mac address-table address 0050.5699.0001` and trace to the port.

## Clearing
`clear ip arp 10.10.0.30` (single) is safe. `clear arp-cache` refreshes all entries (IOS re-ARPs
before deleting on newer releases) but on large L3 switches causes a burst of ARP and glean traffic.

## Verify
- [ ] Target shows a MAC, Age resets on traffic; MAC visible on the expected port.
