---
id: computing-software.systems-network-administration.cisco-networking.ipsec-vti-ikev2-site-to-site
name: ipsec-vti-ikev2-site-to-site
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, vpn, ipsec, vti, ikev2, site-to-site-vpn, route-based-vpn, crypto-ikev2-proposal, ikev2-profile, ipsec-profile, tunnel-mode-ipsec, pre-shared-key, aws-vpn, azure-vpn-gateway, gcm]
level: advanced
status: draft
description: "Build a route-based site-to-site IPsec VPN on IOS XE with IKEv2 and a static VTI: proposal, keyring, profile, IPsec profile, routing over the tunnel, interop with cloud gateways."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_ikevpn/configuration/xe-16/sec-sec-for-vpns-w-ipsec-xe-16-book/sec-ipsec-virt-tunnl.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_ike2vpn/configuration/xe-16/sec-flex-vpn-xe-16-book/sec-cfg-ikev2-flex.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Route-based IPsec with IKEv2 and a VTI

A Virtual Tunnel Interface (VTI) is a routable interface protected by IPsec. Whatever you route
into it is encrypted; no crypto ACLs to keep in sync. Preferred over crypto maps for new builds
and required by most cloud VPN gateways' "route-based" mode.

## Configure (HQ side; branch mirrors)
```
crypto ikev2 proposal PROP-AES256
 encryption aes-gcm-256
 prf sha384
 group 20                         ! ECDH P-384; 19 (P-256) is widely interoperable
crypto ikev2 policy POL
 proposal PROP-AES256
crypto ikev2 keyring KR
 peer BRANCH1
  address 203.0.113.20
  pre-shared-key <PSK_LONG_RANDOM>
crypto ikev2 profile IKEV2-BRANCH1
 match identity remote address 203.0.113.20 255.255.255.255
 identity local address 198.51.100.10
 authentication remote pre-share
 authentication local pre-share
 keyring local KR
 dpd 10 3 periodic
!
crypto ipsec transform-set TS esp-gcm 256
 mode tunnel
crypto ipsec profile IPSEC-BRANCH1
 set transform-set TS
 set ikev2-profile IKEV2-BRANCH1
 set pfs group20
!
interface Tunnel10
 ip address 169.254.10.1 255.255.255.252
 ip mtu 1400
 ip tcp adjust-mss 1360
 tunnel source GigabitEthernet0/0/0
 tunnel destination 203.0.113.20
 tunnel mode ipsec ipv4
 tunnel protection ipsec profile IPSEC-BRANCH1
!
ip route 10.20.0.0 255.255.0.0 Tunnel10     ! or BGP/OSPF over the tunnel
```

## Cloud gateway interop
- AWS/Azure/GCP provide config templates for "Cisco IOS XE (IKEv2, route-based)". Use their
  inside tunnel addresses (169.254.x.x/30) and run BGP over the VTI for dynamic routing.
- Match lifetimes: IKE SA (AWS 28800 s), IPsec SA (3600 s); mismatched proposals are the most
  common failure.
- Behind NAT, IKEv2 switches to UDP 4500 automatically (NAT-T).

## Verify
```
show crypto ikev2 sa                    ! READY state
show crypto ipsec sa interface Tunnel10 ! encaps/decaps counters increasing both ways
show interfaces Tunnel10                ! up/up
ping 169.254.10.2 source Tunnel10
```
- [ ] IKEv2 SA READY; IPsec SA counters increase in both directions.
- [ ] Routes for remote subnets point at Tunnel10.
- [ ] Rekey works: SA survives past the IPsec lifetime without traffic loss.
