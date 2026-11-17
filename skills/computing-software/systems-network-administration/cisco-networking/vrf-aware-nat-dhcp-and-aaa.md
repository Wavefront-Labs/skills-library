---
id: computing-software.systems-network-administration.cisco-networking.vrf-aware-nat-dhcp-and-aaa
name: vrf-aware-nat-dhcp-and-aaa
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, vrf, vrf-aware-services, vrf-aware-nat, dhcp-relay-vrf, aaa-vrf, management-vrf, source-interface]
level: practitioner
status: draft
description: "Make IOS services work in VRFs: VRF-aware NAT, DHCP relay to a server in another VRF, AAA/SNMP/syslog/NTP via a management VRF, and the common traps."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_nat/configuration/xe-16/nat-xe-16-book/iadnat-mpls-vpn.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_dhcp/configuration/xe-16/dhcp-xe-16-book/dhcp-relay-mpls-vpn-suppt.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VRF-aware NAT, DHCP relay and AAA

## NAT
```
ip nat inside source list CUST-A-NAT interface GigabitEthernet0/0 vrf CUST-A overload
ip nat inside source list CUST-B-NAT interface GigabitEthernet0/0 vrf CUST-B overload
ip route vrf CUST-A 0.0.0.0 0.0.0.0 203.0.113.1 global
```
Overlapping inside addresses in different VRFs are fine; translations are keyed by VRF.
`show ip nat translations vrf CUST-A`. NVI (`ip nat enable`) also supports VRFs.

## DHCP relay across VRFs
Client VRF CUST-A, server in global or a services VRF:
```
interface Vlan20
 vrf forwarding CUST-A
 ip helper-address global 10.0.0.67            ! server in global table
 ! or: ip helper-address vrf SERVICES 10.0.0.67
ip dhcp relay information option vpn            ! adds VPN identifier sub-options for the server
```
The server must route back to giaddr (which lives in CUST-A): leak a route or use the
relay's source interface option (`ip dhcp relay source-interface Loopback5`).

## Management services via a management VRF
```
ip vrf forwarding Mgmt-intf                     ! on Gi0 OOB port
aaa group server tacacs+ ISE-TACACS
 server name ISE-1
 ip vrf forwarding Mgmt-intf
 ip tacacs source-interface GigabitEthernet0
aaa group server radius ISE
 ip vrf forwarding Mgmt-intf
logging host 10.0.0.50 vrf Mgmt-intf
snmp-server host 10.0.0.51 vrf Mgmt-intf version 3 priv NMSUSER
ntp server vrf Mgmt-intf 10.0.0.11
ip ssh source-interface GigabitEthernet0
ip domain lookup vrf Mgmt-intf source-interface GigabitEthernet0
copy tftp: flash: vrf Mgmt-intf                 ! or ip tftp source-interface GigabitEthernet0
```

## Traps
- Forgetting `vrf` on a service: it silently uses the global table and times out.
- Source interface in a different VRF from the server: packets never leave.
- SNMP traps need `vrf` on the host line; polling works via any interface with the community/user ACL.
- `ping` and `traceroute` must also be run with `vrf`.

## Verify
- [ ] `test aaa group ...`, `show logging | i Logging to`, `show ntp associations` all show the servers reachable via the VRF.
