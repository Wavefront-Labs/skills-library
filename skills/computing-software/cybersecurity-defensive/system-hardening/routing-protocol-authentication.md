---
id: computing-software.cybersecurity-defensive.system-hardening.routing-protocol-authentication
name: routing-protocol-authentication
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [routing-protocol-authentication, bgp-tcp-ao, ospf-authentication, gtsm, key-chain, network-device-hardening]
level: advanced
status: draft
description: "Authenticate and protect routing protocols: BGP TCP-AO or MD5 with GTSM and max-prefix, OSPF and IS-IS SHA authentication, key chains with rotation, and passive interfaces."
sources: ["https://datatracker.ietf.org/doc/html/rfc5925", "https://datatracker.ietf.org/doc/html/rfc5082", "https://datatracker.ietf.org/doc/html/rfc5709", "https://datatracker.ietf.org/doc/html/rfc7454", "https://www.manrs.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Routing protocol authentication

Unauthenticated routing adjacencies let anyone on the segment inject routes (traffic redirection, blackholing)
or reset sessions. Authenticate every adjacency and limit who can even reach the protocol.

## BGP
- **TCP-AO** (RFC 5925) replaces TCP MD5 (RFC 2385): stronger MACs (HMAC-SHA-1-96, AES-128-CMAC-96), key
  rollover without session reset. Supported on recent IOS XR, Junos and others; use where both ends support it.
- **TCP MD5** remains common on eBGP peering: `neighbor 192.0.2.1 password <secret>` (Cisco IOS),
  `set protocols bgp group EXT neighbor 192.0.2.1 authentication-key "<secret>"` (Junos). Weak by modern
  standards but blocks blind injection and resets.
- **GTSM / TTL security** (RFC 5082): accept eBGP packets only with TTL 255 (directly connected):
  `neighbor 192.0.2.1 ttl-security hops 1` (IOS); Junos `ttl 255` with `multihop` off plus lo0 filter. Spoofed
  packets from far away arrive with lower TTL and are dropped cheaply.
- **Max-prefix** limits, inbound prefix filters (IRR-based, RPKI ROV), and BGP session protection in the
  control-plane filter (only configured peers to TCP/179). MANRS and RFC 7454 cover operational practice.

## OSPF
- OSPFv2: use HMAC-SHA cryptographic authentication (RFC 5709) where supported, else MD5; not plaintext type 1.
  Cisco IOS with key chains:
  ```
  key chain OSPF-KEYS
   key 1
    key-string <secret>
    cryptographic-algorithm hmac-sha-256
  interface Gi0/1
   ip ospf authentication key-chain OSPF-KEYS
  ```
  Junos: `set protocols ospf area 0 interface ge-0/0/1 authentication md5 1 key "<secret>"` or keychain with
  `hmac-sha-256` on newer releases.
- OSPFv3: authentication trailer (RFC 7166) or IPsec.
- **Passive interfaces** on all user-facing and loopback interfaces (`passive-interface default`, then
  `no passive-interface` on core links) so no adjacency forms where it should not.

## IS-IS
HMAC-MD5 (RFC 5304) or HMAC-SHA (RFC 5310) for hellos and LSPs at area and domain levels:
`authentication mode md5` + key chain per level (IOS), `set protocols isis level 2 authentication-key ...` (Junos).

## EIGRP, RIP, VRRP, HSRP
EIGRP: SHA-256 in named mode; RIPv2: MD5; HSRP/VRRP: MD5 authentication to stop gateway hijack on LANs.

## Key management
Per-adjacency or per-domain keys from a vault, key chains with `accept-lifetime`/`send-lifetime` overlaps for
hitless rotation, rotation schedule, no keys in plaintext configs (`service password-encryption` is only
obfuscation; protect config backups).

## Verify
`show ip ospf interface` shows cryptographic authentication enabled; `show bgp neighbors` shows MD5/AO and TTL
security; a test router with the wrong key fails to form an adjacency and the failure is logged.
