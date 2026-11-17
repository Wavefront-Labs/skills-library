---
id: computing-software.systems-network-administration.cisco-networking.sd-wan-centralized-policies-and-aar
name: sd-wan-centralized-policies-and-aar
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-sd-wan, sdwan-centralized-policy, aar-policy, application-aware-routing, sla-class, vsmart, control-policy, data-policy]
level: practitioner
status: draft
description: "Build Cisco SD-WAN centralised policies: control vs data policy, application-aware routing with SLA classes, lists, activation on the controller and verification."
sources:
  - https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/policies/ios-xe-17/policies-book-xe.html
  - https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/policies/ios-xe-17/policies-book-xe/application-aware-routing.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Centralised policies and application-aware routing

## Policy types (SD-WAN Manager > Configuration > Policies)
| Type | Runs on | Controls |
|---|---|---|
| Centralised control policy | Controller (vSmart) | OMP route/TLOC advertisement: topology (hub-and-spoke, regional), service chaining |
| Centralised data policy | pushed to edges | per-flow actions: drop, NAT DIA, next-hop, TLOC preference, service chaining |
| Application-aware routing (AAR) | pushed to edges | path choice per app based on BFD-measured loss/latency/jitter vs SLA class |
| Localised policy | edge | QoS, ACLs, route policy |

## Building blocks (lists)
Site lists, VPN lists, application lists (NBAR-based), prefix lists, TLOC lists, colors.

## AAR example
SLA class `VOICE-SLA`: loss 1%, latency 150 ms, jitter 30 ms.
AAR policy sequence: match app-list `VOICE-APPS` -> SLA class VOICE-SLA, preferred color `mpls`,
fallback to best path. Apply to site list ALL-BRANCHES, VPN 10.
Tunnels are measured by BFD (default hello 1 s, app-route poll interval 10 min, multiplier 6).
Faster reaction: lower `app-route poll-interval` (consider CPU and stability).

## Activation
Centralised policies are activated on the controllers (vSmart must be in vManage mode/templated).
Only one centralised policy active at a time: it contains all control/data/AAR parts.
Edits to an active policy push immediately on save: test in a lab policy first.

## Verify (edge)
```
show sdwan policy from-vsmart                 ! policies received
show sdwan app-route stats                    ! loss/latency/jitter per tunnel
show sdwan app-route sla-class
show sdwan policy app-route-policy-filter     ! counters per sequence
show sdwan omp routes vpn 10                  ! control policy effects
```
Manager: Monitor > Applications and Tunnel health; Simulate Flows tool shows which path a flow takes.

## Gotchas
- AAR only chooses among paths the routing allows; control policy may have hidden the path.
- If no path meets SLA and no fallback is configured, traffic uses any available path (default
  behaviour) or is dropped with `strict` - know which you set.
- Large app lists depend on DPI; first packets may be routed before the app is classified.
