---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-ipsec-site-to-site-vpn
name: pan-os-ipsec-site-to-site-vpn
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [ipsec-tunnel, pan-os, ike-gateway, ikev2, tunnel-interface, crypto-profile, proxy-id, site-to-site-vpn]
level: practitioner
status: draft
description: "Build a PAN-OS site-to-site IPsec VPN with IKE gateway, crypto profiles, tunnel interface, routing and policy, and troubleshoot phase 1 and 2."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/vpns/site-to-site-vpn"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: a routed tunnel to a remote site with strong crypto.

```
configure
set network ike crypto-profiles IKE-STRONG hash sha256 dh-group group14 encryption aes-256-cbc lifetime hours 8
set network ike crypto-profiles IPSEC-STRONG esp authentication sha256 encryption aes-256-gcm
set network ike gateway GW-BRANCH protocol ikev2 local-address interface ethernet1/1 peer-address ip 203.0.113.50
set network ike gateway GW-BRANCH authentication pre-shared-key key <PSK>
set network interface tunnel units tunnel.1 ip 169.254.10.1/30
set zone vpn network layer3 tunnel.1
set network virtual-router default interface tunnel.1
set network tunnel ipsec T-BRANCH auto-key ike-gateway GW-BRANCH ipsec-crypto-profile IPSEC-STRONG
set network tunnel ipsec T-BRANCH tunnel-interface tunnel.1
set network virtual-router default routing-table ip static-route to-branch destination 10.50.0.0/16 interface tunnel.1
commit
```
Name the IKE crypto profile in the gateway's `ikev2 ike-crypto-profile`. Use a long random PSK stored in a vault, or certificates.

Gotchas
- Proxy IDs are needed when the peer is policy-based (third-party firewalls); mismatched traffic selectors cause phase 2 failure.
- Security policy must allow both directions between `vpn` and internal zones; NAT exemption rule for VPN traffic placed above source NAT.
- NAT-T is automatic if a NAT sits between peers; open UDP 500 and 4500.

## Verify
```
test vpn ike-sa gateway GW-BRANCH
test vpn ipsec-sa tunnel T-BRANCH
show vpn ike-sa
show vpn ipsec-sa
show vpn flow
```
Phase 1/2 should be established and `show vpn flow` counters increment as traffic crosses. Use `less mp-log ikemgr.log` (confirm) for negotiation errors.
