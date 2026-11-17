---
id: computing-software.systems-network-administration.cisco-networking.ios-dhcp-server-pool
name: ios-dhcp-server-pool
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-dhcp, ip-dhcp-pool, dhcp-pool, dhcp-excluded-address, dhcp-binding, dhcp-conflict, dhcp-reservation, client-identifier, default-router, lease, ip-dhcp-ping-packets, dhcp-database-agent]
level: practitioner
status: draft
description: "Run DHCP on an IOS router or switch for a branch: pools, excluded ranges, options, manual bindings, conflict detection, binding database persistence and troubleshooting."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_dhcp/configuration/xe-16/dhcp-xe-16-book/config-dhcp-server.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DHCP server pools on IOS

Good for branches and small sites; for anything larger use a central server (Kea, Windows) with
relays.

## Configure
```
ip dhcp excluded-address 10.20.10.1 10.20.10.20      ! gateways, printers, APs
ip dhcp pool VLAN10
 network 10.20.10.0 255.255.255.0
 default-router 10.20.10.1
 dns-server 10.0.0.53 10.0.0.54
 domain-name branch.corp.example
 lease 1                                             ! days [hours] [minutes]
 option 43 hex f104.0a00.0a0a                        ! WLC discovery, if needed
!
ip dhcp pool PRINTER-01                              ! manual binding (reservation)
 host 10.20.10.50 255.255.255.0
 client-identifier 0100.50b6.1234.56                 ! 01 + MAC for Ethernet clients
 default-router 10.20.10.1
```
Windows and most clients send client-identifier `01` + MAC; some (Linux NetworkManager, phones)
use a DUID-based ID, in which case use `hardware-address 0050.b612.3456` instead.

## Conflicts and persistence
- The server pings an address before offering (`ip dhcp ping packets 2`, timeout 500 ms). A
  reply logs a conflict and skips the address. `show ip dhcp conflict`, clear with
  `clear ip dhcp conflict *`.
- Bindings live in RAM: a reload forgets them and may hand out in-use addresses (ping check
  helps). Persist: `ip dhcp database flash:dhcp-bindings.txt write-delay 300`, or disable
  conflict logging only if you have a database agent.

## Troubleshoot
```
show ip dhcp pool VLAN10          ! utilisation, next address
show ip dhcp binding
show ip dhcp server statistics
debug ip dhcp server packet       ! DISCOVER/OFFER/REQUEST/ACK per client
```
No offers: the interface facing clients must have an IP in the pool's network (or the relay
`giaddr` must fall in it); `service dhcp` must not be disabled; pool exhausted.

## Gotchas
- Excluded addresses are global, not per pool.
- `network` with a mask must match the interface subnet exactly for directly attached clients.
- Using the router as DHCP server and also `ip helper-address` on the same SVI sends clients two offers.

## Verify
- [ ] Client gets an address outside the excluded range with the right options.
- [ ] `show ip dhcp binding` lists it; reservation clients get their fixed IP.
- [ ] After a reload, bindings are restored from the database file.
