---
id: computing-software.systems-network-administration.cisco-networking.flexvpn-ikev2
name: flexvpn-ikev2
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, flexvpn, ikev2, ipsec, dvti, ikev2-profile, ikev2-authorization-policy, hub-and-spoke, remote-access-vpn]
level: practitioner
status: draft
description: "Build FlexVPN on IOS XE: IKEv2 proposals/policies/profiles, hub DVTI with virtual-template, spoke SVTI, IKEv2 routing and optional spoke-to-spoke NHRP."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_ike2vpn/configuration/xe-16/sec-flex-vpn-xe-16-book.html
  - https://www.cisco.com/c/en/us/support/docs/security/flexvpn/116413-configure-flexvpn-00.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FlexVPN

## Pieces
IKEv2 proposal -> policy -> keyring -> profile; IPsec profile references the IKEv2 profile;
tunnels are virtual tunnel interfaces (static on spokes, dynamic from a virtual-template on the hub).

## Hub
```
crypto ikev2 keyring KR
 peer SPOKES
  address 0.0.0.0 0.0.0.0
  pre-shared-key <PSK>              ! or certificates (preferred at scale)
aaa new-model
aaa authorization network FLEX local
crypto ikev2 authorization policy FLEX-POL
 route set interface                ! push hub tunnel IP route to spokes
 route set access-list FLEX-ROUTES  ! push LAN prefixes
crypto ikev2 profile FLEX-HUB
 match identity remote fqdn domain example.net
 identity local fqdn hub.example.net
 authentication remote pre-share
 authentication local pre-share
 keyring local KR
 aaa authorization group psk list FLEX FLEX-POL
 virtual-template 1
crypto ipsec profile FLEX-IPSEC
 set ikev2-profile FLEX-HUB
interface Loopback100
 ip address 172.31.0.1 255.255.255.255
interface Virtual-Template1 type tunnel
 ip unnumbered Loopback100
 tunnel protection ipsec profile FLEX-IPSEC
```

## Spoke
```
crypto ikev2 profile FLEX-SPOKE
 match identity remote fqdn hub.example.net
 identity local fqdn spoke1.example.net
 authentication remote pre-share
 authentication local pre-share
 keyring local KR
 aaa authorization group psk list FLEX FLEX-POL
crypto ipsec profile FLEX-IPSEC
 set ikev2-profile FLEX-SPOKE
interface Tunnel0
 ip address negotiated              ! or static / unnumbered
 tunnel source GigabitEthernet0/0
 tunnel destination 203.0.113.1
 tunnel protection ipsec profile FLEX-IPSEC
```
Routing: IKEv2 route exchange (above) or a dynamic protocol (BGP/EIGRP) over the tunnels.
Spoke-to-spoke: NHRP on the virtual-template and tunnels (`ip nhrp network-id`, `ip nhrp redirect`
on hub, `ip nhrp shortcut` on spokes).

## Gotchas
- IKEv2 smart defaults exist (default proposal/policy); define your own to enforce strong crypto
  (AES-GCM-256, SHA-384, DH group 19/20/21).
- Identity mismatches are the top failure: match exactly what the peer sends.
- Virtual-access interfaces are cloned per spoke; configuration on Virtual-Template only.

## Verify
```
show crypto ikev2 sa detailed
show crypto session detail
show interfaces virtual-access 1
debug crypto ikev2                       ! briefly
```
