---
id: computing-software.networking-hardware-and-wireless.juniper-junos.ipsec-vpn
name: ipsec-vpn
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, ipsec-vpn, ike-gateway, st0, route-based-vpn]
level: practitioner
status: draft
description: "Build an SRX route-based site-to-site IPsec VPN with IKE proposal/policy/gateway, IPsec policy, st0 tunnel and routing."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Route-based IPsec VPN on SRX
Goal: bring up a tunnel and send traffic through st0.

```
set security ike proposal IKEP authentication-method pre-shared-keys dh-group group14 authentication-algorithm sha-256 encryption-algorithm aes-256-cbc
set security ike policy IKEPOL mode main proposals IKEP pre-shared-key ascii-text "<redacted>"
set security ike gateway GW1 ike-policy IKEPOL address 203.0.113.50 external-interface ge-0/0/0.0
set security ipsec proposal IPSECP protocol esp encryption-algorithm aes-256-cbc authentication-algorithm hmac-sha-256-128
set security ipsec policy IPSECPOL proposals IPSECP
set security ipsec vpn VPN1 bind-interface st0.0 ike gateway GW1 ipsec-policy IPSECPOL
set security ipsec vpn VPN1 establish-tunnels immediately
set interfaces st0 unit 0 family inet address 10.255.255.1/30
set security zones security-zone vpn interface st0.0
set routing-options static route 192.0.2.0/24 next-hop st0.0
```

- Policy needs entries in both directions between the LAN and vpn zones.
- Proposal sets must match both ends exactly; algorithms vary by release: confirm.

Gotcha: Phase 1 up but Phase 2 down is usually mismatching proxy-IDs (route-based to a policy-based peer) or missing st0 route.

## Verify
- `show security ike security-associations` and `show security ipsec security-associations` show both SAs; `ping 192.0.2.1 source 10.0.0.1` crosses the tunnel.
