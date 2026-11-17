---
id: computing-software.systems-network-administration.cisco-networking.gre-over-ipsec-tunnel-protection
name: gre-over-ipsec-tunnel-protection
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, gre-over-ipsec, tunnel-protection, ipsec-profile, ikev2, transport-mode, routing-over-vpn]
level: practitioner
status: draft
description: "Run routing protocols over an encrypted tunnel with GRE over IPsec using tunnel protection: IKEv2 profile, transport mode, MTU/MSS, OSPF over the tunnel, and verification."
sources:
  - https://www.cisco.com/c/en/us/support/docs/security-vpn/ipsec-negotiation-ike-protocols/14012-gre-ipsec.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_ikevpn/configuration/xe-16/sec-ike-for-ipsec-vpns-xe-16-book.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GRE over IPsec with tunnel protection

GRE carries multicast and routing protocols; IPsec encrypts. `tunnel protection` binds an IPsec
profile to a tunnel interface so the crypto follows the tunnel (no crypto maps, no proxy ACLs).

## Configuration (site A; mirror on site B)
```
crypto ikev2 keyring KR
 peer SITE-B
  address 198.51.100.2
  pre-shared-key local Str0ngKey! 
  pre-shared-key remote Str0ngKey!
crypto ikev2 profile IKEV2-PROF
 match identity remote address 198.51.100.2 255.255.255.255
 authentication remote pre-share
 authentication local pre-share
 keyring local KR
crypto ipsec transform-set TS esp-gcm 256
 mode transport                        ! GRE already adds an outer IP header
crypto ipsec profile IPSEC-PROF
 set transform-set TS
 set ikev2-profile IKEV2-PROF

interface Tunnel0
 ip address 172.31.0.1 255.255.255.252
 ip mtu 1400
 ip tcp adjust-mss 1360
 tunnel source GigabitEthernet0/0/0
 tunnel destination 198.51.100.2
 tunnel protection ipsec profile IPSEC-PROF
 ip ospf network point-to-point
router ospf 1
 network 172.31.0.0 0.0.0.3 area 0
```
Default IKEv2 proposals (smart defaults) are used if none is defined; define explicit proposals in
production to control algorithms.

## Avoid recursive routing
The tunnel destination must be reached via the underlay (default route to the ISP), never via the
tunnel. Do not advertise the public addresses into OSPF over the tunnel; otherwise
`%TUN-5-RECURDOWN` and flapping.

## Verify
```
show crypto ikev2 sa
show crypto ipsec sa interface Tunnel0 | include pkts|Status
show interfaces Tunnel0 | include line protocol
show ip ospf neighbor
```
Encrypt/decrypt counters must both increase; one direction only = asymmetric policy or NAT issue.

## Gotchas
- NAT in the path: NAT-T (UDP 4500) is automatic; transport mode with NAT works for GRE/IPsec on
  IOS XE, but some third-party peers need tunnel mode.
- Keepalives on GRE (`keepalive 10 3`) or BFD/OSPF timers detect a dead peer; IPsec DPD keeps
  SAs clean (`dpd 10 2 on-demand` in the IKEv2 profile).
- VTI (`tunnel mode ipsec ipv4`) is simpler when you do not need multicast-capable GRE or
  non-IP payloads; it saves 4-24 bytes.

## Verify
- [ ] OSPF FULL over Tunnel0 and SAs show increasing encaps/decaps.
