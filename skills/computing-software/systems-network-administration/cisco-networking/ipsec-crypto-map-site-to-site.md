---
id: computing-software.systems-network-administration.cisco-networking.ipsec-crypto-map-site-to-site
name: ipsec-crypto-map-site-to-site
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, vpn, ipsec, crypto-map, ikev1, ikev2, interesting-traffic, transform-set, nat-exemption]
level: practitioner
status: draft
description: "Build a policy-based IPsec site-to-site VPN on IOS with a crypto map: IKEv2 proposal, transform set, crypto ACL mirroring and NAT exemption, for third-party peers."
sources:
  - https://www.cisco.com/c/en/us/support/docs/security-vpn/ipsec-negotiation-ike-protocols/117337-config-asa-router-00.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_ikevpn/configuration/xe-16/sec-sec-for-vpns-w-ipsec-xe-16-book/sec-cfg-vpn-ipsec.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Policy-based IPsec with a crypto map

Use a crypto map when the far end is a third-party firewall that only does policy-based
(traffic-selector) VPNs. For router-to-router, prefer route-based VTIs.

```
crypto ikev2 proposal P1
 encryption aes-cbc-256
 integrity sha256
 group 19
crypto ikev2 policy POL1
 proposal P1
crypto ikev2 keyring KR
 peer FW-B
  address 198.51.100.20
  pre-shared-key <PSK>
crypto ikev2 profile PROF-B
 match identity remote address 198.51.100.20 255.255.255.255
 authentication remote pre-share
 authentication local pre-share
 keyring local KR
crypto ipsec transform-set TS esp-aes 256 esp-sha256-hmac
 mode tunnel
ip access-list extended VPN-B
 permit ip 10.1.0.0 0.0.255.255 10.2.0.0 0.0.255.255
crypto map CMAP 10 ipsec-isakmp
 set peer 198.51.100.20
 set transform-set TS
 set ikev2-profile PROF-B
 set pfs group19
 match address VPN-B
interface GigabitEthernet0/0/0
 crypto map CMAP
```

## Rules that bite
- The crypto ACL must be an **exact mirror** of the peer's (source/destination swapped). A
  mismatch shows as Phase 2 "proxy identities not supported" / TS_UNACCEPTABLE.
- Exempt VPN traffic from NAT (deny it in the NAT ACL/route-map), or packets are translated
  before encryption and never match the crypto ACL.
- A route for the remote subnet must point out the crypto-map interface (usually the default route).
- One SA pair per ACL line: with many lines, many SAs. Summarise if both sides agree.
- Lifetimes: IOS default 86400 s (IKE) / 3600 s (IPsec); match the peer to avoid rekey drops.

## Verify
```
show crypto ikev2 sa
show crypto ipsec sa peer 198.51.100.20   ! encaps/decaps counters must both rise
show crypto map
```
- [ ] Ping from an inside host (not the router) brings up the tunnel; encaps and decaps increment.
