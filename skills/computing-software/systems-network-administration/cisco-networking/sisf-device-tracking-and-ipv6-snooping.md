---
id: computing-software.systems-network-administration.cisco-networking.sisf-device-tracking-and-ipv6-snooping
name: sisf-device-tracking-and-ipv6-snooping
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, catalyst-9000, sisf, device-tracking, ipv6-snooping, ip-device-tracking, binding-table, duplicate-address]
level: practitioner
status: draft
description: "Configure SISF device tracking on Catalyst 9000: policies, the binding table, IPv6 snooping, and fixing the classic 0.0.0.0 probe duplicate-address problem."
sources:
  - https://www.cisco.com/c/en/us/support/docs/switches/catalyst-9300-series-switches/217927-understand-sisf-on-catalyst-9000-series.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_sisf_based_device_tracking.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SISF device tracking and IPv6 snooping

## What SISF is
Switch Integrated Security Features: one framework that learns IP/MAC/port bindings (ARP, ND,
DHCP, DHCPv6 gleaning) into a **binding table** used by 802.1X/ISE (IP for sessions), IPv6 First Hop
Security (RA guard, ND inspection, source guard), LISP/SD-Access, and Catalyst Center.

## Enable
```
device-tracking policy DT-ACCESS
 tracking enable
 limit address-count 10
 no protocol udp                       ! do not glean from arbitrary UDP
 security-level glean
interface range Gi1/0/1 - 48
 device-tracking attach-policy DT-ACCESS
device-tracking policy DT-TRUNK
 trusted-port
 device-role switch
 no protocol udp
interface Te1/1/1
 device-tracking attach-policy DT-TRUNK
```
Features like 802.1X with ISE may auto-attach `DT-PROGRAMMATIC`; a custom policy overrides it.

## The 0.0.0.0 probe / duplicate address problem
Device tracking probes hosts with ARP probes sourced from 0.0.0.0 (RFC 5227) to check liveness.
Windows hosts sometimes see this as an address conflict (duplicate IP warnings) if they are just
coming up. Fixes:
```
device-tracking policy DT-ACCESS
 tracking enable reachable-lifetime 300
ip device tracking probe auto-source fallback 0.0.0.253 255.255.255.0 override   ! legacy syntax
device-tracking tracking auto-source fallback 0.0.0.253 255.255.255.0           ! SISF syntax: source from SVI or x.x.x.253
```
`auto-source` makes probes use the SVI address (or a fallback host address in the subnet) instead of 0.0.0.0.

## IPv6 snooping
SISF gleans ND/DHCPv6 to bind IPv6 addresses; with `security-level guard` it drops ND messages
that conflict with existing bindings (ND inspection).

## Verify
```
show device-tracking policies
show device-tracking database                   ! IPv4/IPv6 bindings, state REACHABLE/STALE
show device-tracking counters interface Gi1/0/5
```
- [ ] Bindings for known hosts present; trunk ports trusted; no duplicate-address complaints from Windows clients.
