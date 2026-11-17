---
id: computing-software.systems-network-administration.network-design.secondary-ip-addresses
name: secondary-ip-addresses
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, secondary-address, ipv4-addressing, multinetting, address-migration]
level: practitioner
status: draft
description: "Use secondary IPv4 addresses on router and host interfaces correctly: temporary migration and multinetting, routing-protocol and DHCP side effects, and getting rid of them."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13788-3.html
  - https://www.cisco.com/c/en/us/td/docs/routers/ios/config/17-x/ip-addressing/b-ip-addressing/m_ipv4-adressing.html
  - https://man7.org/linux/man-pages/man8/ip-address.8.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secondary IP addresses

## When they are legitimate
- **Renumbering**: add the new subnet as secondary on the gateway, move hosts, then swap primary.
- **Running out of space** on a VLAN temporarily before resizing.
- Hosts: extra service IPs (web vhosts, keepalived VIP shows as secondary on Linux).

## Router configuration
```
interface Vlan20
 ip address 10.20.0.1 255.255.255.0
 ip address 10.21.0.1 255.255.255.0 secondary
```
Traffic between the two subnets on the same VLAN hairpins through the router (and generates ICMP
redirects; add `no ip redirects`).

## Side effects
- **DHCP**: the relay (`ip helper-address`) sends `giaddr` = primary address, so the server offers
  from the primary scope only. To serve the secondary range, configure a shared network / superscope
  (ISC `shared-network`, Windows superscope, Kea `shared-networks`).
- **OSPF**: forms adjacencies only over the primary subnet; secondaries are advertised as stub
  networks if covered by a network statement / `ip ospf area`. EIGRP sources hellos from the primary;
  neighbours on the secondary subnet will not form.
- **HSRP/VRRP**: add `standby 1 ip 10.21.0.254 secondary` for the extra subnet.
- **Firewalls/ACLs** written for the primary subnet do not cover the secondary.

## Linux and Windows
```
ip addr add 10.21.0.10/24 dev eth0 label eth0:1   # secondary
ip -4 addr show dev eth0                          # 'secondary' flag listed
```
On Linux, removing the primary deletes secondaries in the same subnet unless
`net.ipv4.conf.all.promote_secondaries=1`. On Windows, added addresses are all equal; source
address selection may pick any, so set `SkipAsSource` on service IPs:
`Set-NetIPAddress -IPAddress 10.21.0.10 -SkipAsSource $true`.

## Exit plan
Secondaries should be temporary: record the removal date, migrate, then remove and clean DHCP and
ACLs.

## Verify
- [ ] Hosts on both subnets get DHCP leases, reach each other and the internet, and no routing adjacency changed.
