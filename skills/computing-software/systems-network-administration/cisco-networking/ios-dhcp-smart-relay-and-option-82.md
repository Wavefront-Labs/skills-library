---
id: computing-software.systems-network-administration.cisco-networking.ios-dhcp-smart-relay-and-option-82
name: ios-dhcp-smart-relay-and-option-82
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, dhcp, smart-relay, dhcp-relay, relay-information-option, option-82, giaddr, secondary-subnet]
level: practitioner
status: draft
description: "Use IOS DHCP smart relay to serve secondary subnets, and configure relay agent information (option 82) insertion, trust and policies correctly."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_dhcp/configuration/xe-16/dhcp-xe-16-book/config-dhcp-relay-agent.html
  - https://datatracker.ietf.org/doc/html/rfc3046
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DHCP smart relay and the relay information option

## Smart relay
When an SVI has primary and secondary subnets, the relay always uses the **primary** address as
giaddr. If the primary scope fills, clients get nothing. Smart relay switches giaddr to the
secondary address after three unanswered DISCOVERs from the same client.
```
ip dhcp smart-relay
interface Vlan10
 ip address 10.10.0.1 255.255.255.0
 ip address 10.10.1.1 255.255.255.0 secondary
 ip helper-address 10.0.0.67
```
The server needs scopes for both subnets (Windows: a superscope).

## Relay information option (option 82)
The relay can add circuit-id/remote-id so the server knows where the request came from.
```
ip dhcp relay information option                 ! insert option 82 on relayed packets
ip dhcp relay information check                  ! validate on replies (default on)
ip dhcp relay information policy keep            ! what to do if client packet already has 82: drop|keep|replace
ip dhcp relay information trust-all              ! or per interface: ip dhcp relay information trusted
```
Per interface on IOS XE: `ip dhcp relay information option-insert`.

## Interaction with DHCP snooping
- A snooping access switch inserts option 82 with giaddr 0.0.0.0. The upstream relay/server sees
  option 82 with zero giaddr from an untrusted interface and drops it:
  `DHCPD: inconsistent relay information`.
- Fix on the relay: `ip dhcp relay information trusted` on the SVI/interface (or `trust-all`), or on IOS
  DHCP server `ip dhcp relay information trust-all`; or stop insertion on the access switch
  (`no ip dhcp snooping information option`).

## Verify
```
show ip dhcp relay information trusted-sources
debug ip dhcp server packet detail          ! shows option 82 sub-options
```
- [ ] Clients on the secondary subnet get leases after the primary pool fills (test with a tiny primary scope).
