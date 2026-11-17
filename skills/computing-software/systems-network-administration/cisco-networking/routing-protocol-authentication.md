---
id: computing-software.systems-network-administration.cisco-networking.routing-protocol-authentication
name: routing-protocol-authentication
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, routing-authentication, ospf-authentication, eigrp-authentication, bgp-tcp-ao, key-chain, hmac-sha]
level: practitioner
status: draft
description: "Authenticate OSPF, EIGRP and BGP neighbours on IOS with key chains and HMAC-SHA, rotate keys without dropping adjacencies, and diagnose mismatches."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/configuration/xe-16/iro-xe-16-book/iro-ospfv2-crypto-authen.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_eigrp/configuration/xe-16/ire-xe-16-book/ire-sha-256.html
  - https://www.rfc-editor.org/rfc/rfc5709
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Routing protocol authentication

Stops rogue or accidental neighbours injecting routes. MD5 still works but is legacy; use
HMAC-SHA where both sides support it.

## Key chain with overlapping lifetimes (rotation without outage)
```
key chain RP-KEYS
 key 1
  key-string <OLD_KEY>
  cryptographic-algorithm hmac-sha-256
  send-lifetime 00:00:00 Jan 1 2026 00:00:00 Dec 1 2026
  accept-lifetime 00:00:00 Jan 1 2026 00:00:00 Dec 15 2026
 key 2
  key-string <NEW_KEY>
  cryptographic-algorithm hmac-sha-256
  send-lifetime 00:00:00 Dec 1 2026 infinite
  accept-lifetime 00:00:00 Nov 15 2026 infinite
```
Accept windows overlap send windows so both ends accept either key during the change.
Lifetimes depend on correct clocks: NTP first.

## OSPF (RFC 5709 HMAC-SHA)
```
interface Te1/1/1
 ip ospf authentication key-chain RP-KEYS
```
## EIGRP named mode
```
router eigrp CORP
 address-family ipv4 autonomous-system 100
  af-interface default
   authentication mode hmac-sha-256 <PASSWORD>
```
## BGP
```
router bgp 64512
 neighbor 203.0.113.1 password <MD5_KEY>         ! TCP MD5, universal
 ! or TCP-AO where supported:  neighbor 203.0.113.1 ao <KEYCHAIN>
```
Changing a BGP MD5 password resets nothing immediately, but the session drops at the next
TCP reset unless both sides change within the hold time.

## Diagnose
- OSPF: `debug ip ospf adj` -> "Mismatched Authentication type/Key"; neighbour never appears.
- EIGRP: `%DUAL-5-NBRCHANGE ... authentication failure`.
- BGP: `%TCP-6-BADAUTH Invalid MD5 digest` / `No MD5 digest`.

## Verify
```
show ip ospf interface Te1/1/1 | include auth|key
show key chain
show ip bgp neighbors 203.0.113.1 | include md5|Option
```
- [ ] Every routing adjacency authenticated; key rotation rehearsed without drops.
