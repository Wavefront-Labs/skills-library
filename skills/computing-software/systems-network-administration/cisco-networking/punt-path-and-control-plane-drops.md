---
id: computing-software.systems-network-administration.cisco-networking.punt-path-and-control-plane-drops
name: punt-path-and-control-plane-drops
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, punt-path, control-plane, copp, punt-policer, cpu-bound-traffic, lsmpi, catalyst-9000-fed]
level: practitioner
status: draft
description: "Diagnose traffic punted to the CPU on IOS XE routers and Catalyst 9000: punt causes, punt policer and CoPP drops, and fixing what keeps punting."
sources:
  - https://www.cisco.com/c/en/us/support/docs/switches/catalyst-9300-series-switches/215843-troubleshoot-high-cpu-on-catalyst-9000-switches.html
  - https://www.cisco.com/c/en/us/support/docs/routers/asr-1000-series-aggregation-services-routers/200736-Punt-Path-Troubleshooting-on-ASR1000.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Punted traffic and control-plane drops

## What punting is
The hardware forwards most traffic. Packets it cannot handle are punted to the CPU: traffic to
the device, routing protocols, ARP, TTL-expired, IP options, ACL `log` hits, packets needing ARP
resolution (glean), unsupported features, MTU/fragmentation, redirects.
Too much punting -> high CPU, dropped control traffic, flapping protocols.

## Catalyst 9000
```
show platform software fed switch active punt cause summary     ! counters per cause
show platform software fed switch active punt cpuq brief        ! per CPU queue rx/drops
show platform software fed switch active cpu-interface
show policy-map control-plane                                    ! CoPP class drops
monitor capture CPU control-plane in match any buffer size 10    ! capture punted packets
monitor capture CPU start / stop ; show monitor capture CPU buffer brief
```

## IOS XE routers (QFP)
```
show platform hardware qfp active infrastructure punt statistics type per-cause
show platform hardware qfp active infrastructure punt statistics type punt-drop
show platform software infrastructure lsmpi                      ! punt path to IOSd
show platform hardware qfp active statistics drop | include Punt
```

## Common causes and fixes
| Cause | Fix |
|---|---|
| Glean/ARP for many unresolved hosts (scans) | null-route unused ranges, `ip arp incomplete` throttles |
| TTL expired (routing loop, traceroute floods) | fix the loop; CoPP limits ICMP |
| IP redirects (traffic hairpins same interface) | `no ip redirects`, fix design |
| ACL with `log` on busy entries | remove `log` or use `log-input` rate-limited |
| IP options / fragments | drop at edge (`ip options drop`) |
| Unsupported feature path (e.g. NAT on platform without hardware NAT) | redesign |

## CoPP drops are not always bad
CoPP drops protect the CPU. A drop counter rising in a "default/unknown" class during an
attack is CoPP working; rising in the routing protocol class means you are losing control traffic.

## Verify
- [ ] Punt cause counters steady at baseline; CPU normal; no drops in critical CoPP classes.
