---
id: computing-software.systems-network-administration.cisco-networking.debugging-ios-dhcp-server-and-relay
name: debugging-ios-dhcp-server-and-relay
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, dhcp, debug-ip-dhcp, dhcp-relay, ip-helper-address, dhcp-troubleshooting, dhcp-conflict]
level: practitioner
status: draft
description: "Debug IOS DHCP server and relay problems: debug ip dhcp server packet/events, relay giaddr checks, conflicts, exhausted pools and the usual root causes."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/dynamic-address-allocation-resolution/27470-100.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_dhcp/configuration/xe-16/dhcp-xe-16-book.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Debugging DHCP server and relay on IOS

## Server side
```
show ip dhcp pool                      ! utilisation, next available address
show ip dhcp binding
show ip dhcp conflict                  ! addresses found in use by ping/gratuitous ARP
show ip dhcp server statistics         ! DISCOVER/OFFER/REQUEST/ACK/NAK counts
debug ip dhcp server events
debug ip dhcp server packet detail
```
Reading packet debug:
- `DHCPD: DHCPDISCOVER received from client 0100.5056.aa01.02 on interface Vlan10` - arrived.
- `DHCPD: Sending DHCPOFFER to client ... (10.10.0.20)` - offered.
- No offer: no pool matches the receiving interface subnet (or giaddr), pool exhausted, or
  address excluded. `DHCPD: no address pool for ...` in events.

Clear conflicts after fixing their cause: `clear ip dhcp conflict *`.

## Relay side
```
interface Vlan20
 ip helper-address 10.0.0.67
debug ip dhcp server packet            ! on the relay: shows "relay" forwarding
show ip interface Vlan20 | include Helper
```
The relay sets **giaddr** to the receiving interface's primary IP. The server picks the pool by
giaddr. Common failures:
- Server has no scope for the giaddr subnet.
- Return path: server cannot route back to giaddr (missing route, firewall UDP 67).
- Secondary addresses on the SVI: giaddr is the primary only, unless `ip dhcp smart-relay`.
- `ip helper-address` also forwards other UDP broadcasts (TFTP, DNS, NetBIOS...) unless
  `no ip forward-protocol udp <port>`.

## Other root causes
- DHCP snooping dropping offers: trusted port missing on the uplink, or option 82 inserted and
  rejected (`show ip dhcp snooping statistics`).
- Client in wrong VLAN, PortFast missing (STP delay outlasts client timeout).
- Lease time too long on a busy guest VLAN: pool exhausted with stale leases.

## Verify
- [ ] Packet capture or debug shows DORA complete with expected giaddr and pool.
- [ ] `show ip dhcp server statistics` NAK and conflict counts not climbing.
