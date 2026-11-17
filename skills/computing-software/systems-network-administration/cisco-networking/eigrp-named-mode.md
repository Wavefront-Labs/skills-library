---
id: computing-software.systems-network-administration.cisco-networking.eigrp-named-mode
name: eigrp-named-mode
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, eigrp, eigrp-named-mode, address-family, af-interface, topology-base, wide-metrics, eigrp-authentication, hmac-sha-256, passive-interface, eigrp-neighbors, classic-mode]
level: practitioner
status: draft
description: "Configure EIGRP in named mode on IOS: address families, af-interface settings, wide metrics, SHA-256 auth, passive defaults, migrating from classic mode and neighbour checks."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_eigrp/configuration/xe-16/ire-xe-16-book/ire-named-eigrp.html
  - https://datatracker.ietf.org/doc/html/rfc7868
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EIGRP named mode

Named mode puts all EIGRP settings (per-interface too) under one `router eigrp NAME` block,
supports IPv4 and IPv6 address families together and uses 64-bit wide metrics.

## Configure
```
router eigrp CORP
 address-family ipv4 unicast autonomous-system 100
  eigrp router-id 10.0.0.1
  network 10.0.0.0 0.255.255.255
  af-interface default
   passive-interface                    ! passive everywhere by default
  exit-af-interface
  af-interface TenGigabitEthernet1/1/1
   no passive-interface
   authentication mode hmac-sha-256 <AUTH_KEY>
   hello-interval 1
   hold-time 3
  exit-af-interface
  topology base
   maximum-paths 4
   variance 1
  exit-af-topology
 exit-address-family
 address-family ipv6 unicast autonomous-system 100
  ! IPv6 runs on all interfaces with an IPv6 address by default
 exit-address-family
```
Neighbours need the same AS number and K values; the name is local only.

## Wide metrics
Named mode computes with 64-bit metric (picosecond delay), so 10G/40G/100G links differ.
Values put into the RIB are scaled down by `metric rib-scale` (default 128). Classic-mode
neighbours interoperate, but mixed networks can choose different paths; migrate whole areas.

## Migrate from classic
```
router eigrp 100
 eigrp upgrade-cli CORP           ! converts the classic config in place, no adjacency reset
```
Then `show run | s router eigrp` to review.

## Check
```
show eigrp address-family ipv4 neighbors
show eigrp address-family ipv4 topology
show eigrp address-family ipv4 interfaces detail
show ip route eigrp
show ip protocols | s eigrp            ! K values, router-id, networks
```
`show ip eigrp ...` commands still work for the IPv4 AF.

## Gotchas
- Adjacency fails silently on K-value mismatch (log `%DUAL-5-NBRCHANGE ... K-value mismatch`),
  AS mismatch, authentication mismatch, or subnets not matching (secondary addresses).
- Passive interfaces send no hellos: their subnets are advertised, no neighbours form.
- Use key chains (`authentication key-chain`) with send/accept lifetimes for rotation.

## Verify
- [ ] Neighbours up with expected uptime and SRTT; Q Cnt 0.
- [ ] Routes learned as D / D EX with sensible metrics.
- [ ] Authentication mismatch test brings the neighbour down (proves it is enforced).
