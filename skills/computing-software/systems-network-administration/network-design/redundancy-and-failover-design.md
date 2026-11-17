---
id: computing-software.systems-network-administration.network-design.redundancy-and-failover-design
name: redundancy-and-failover-design
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, redundancy, high-availability, ha, failover, spof, single-point-of-failure, shared-fate, availability-math, nines, fhrp, vrrp, hsrp, glbp, preemption, object-tracking, mlag, vpc, stackwise, switch-stacking, ecmp, routed-access, spanning-tree, bfd, convergence, dual-isp, multihoming, path-diversity, a-b-power, ups, n-plus-1, failover-testing]
level: advanced
status: draft
description: "Design networks that fail over: SPOF and shared-fate analysis, availability maths, VRRP/HSRP with tracking, stacking vs MLAG vs routed ECMP, BFD convergence budgets, diverse paths, failover tests."
sources:
  - https://datatracker.ietf.org/doc/html/rfc5798
  - https://datatracker.ietf.org/doc/html/rfc5880
  - https://datatracker.ietf.org/doc/html/rfc9568
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Redundancy and failover design — two of everything is not the same as no single point of failure

**Goal:** a network where any one component (link, device, power feed, provider) can fail
with a known, short interruption, and where you have proved it by breaking things on
purpose. Protocol configuration details live in the vendor skills (e.g.
`computing-software.systems-network-administration.cisco-networking.routing-protocol-configuration-ospf-and-bgp`).

## 1. Start from the requirement, not the kit
For each service, write down: tolerable outage per failure (e.g. "< 5 s for voice, < 60 s
for file shares") and tolerable total downtime per year. Availability maths:

| Availability | Downtime/year |
|---|---|
| 99.9% | ~8.8 h |
| 99.99% | ~53 min |
| 99.999% | ~5 min |

- Components **in series** multiply: three 99.9% boxes in a chain ≈ 99.7%.
- Components **in parallel** (truly independent): 1 − (1 − A)², so two 99.9% paths ≈ 99.9999%.
- The parallel figure is fiction if the two paths share fate. That is the whole design job.

## 2. Hunt shared fate
Walk the path from user to service and list for every redundant pair what they still share:
- **Physical:** same conduit, same building entry, same patch panel, same "diverse" fibre
  that the carrier routed through one duct. Ask carriers for route maps (KMZ) in writing.
- **Power:** both PSUs on one PDU or UPS; both switches on one circuit. Use A/B feeds from
  separate UPSes.
- **Control plane:** a switch stack or a chassis is one brain. A bad firmware or a stack
  split can take down both "redundant" members.
- **Config and software:** the same bad change pushed to both firewalls at once. Stagger
  changes; keep one side one release behind during upgrades.
- **Provider:** two ISPs who share the last-mile cable or upstream. Check the physical
  entrance and the AS paths.

## 3. First-hop redundancy (hosts' default gateway)
- **VRRP** (standard) or **HSRP** (Cisco) gives hosts one virtual gateway IP shared by two
  routers/L3 switches.
- Align the active gateway with the STP root for that VLAN so traffic does not hairpin.
- Enable **preemption with a delay** (e.g. 60–180 s) so the primary takes back over only
  after its routing has converged; without the delay it blackholes traffic on reboot.
- **Track the uplink** (object tracking / priority decrement) so a gateway whose upstream
  is dead hands over, rather than staying active and dropping everything.
- Default hello/hold timers fail over in ~3–10 s; sub-second timers or BFD where voice
  needs it, at CPU cost.

## 4. Layer 2 vs layer 3 redundancy
| Option | Pros | Cons |
|---|---|---|
| Switch **stack** | simple, one config, cross-stack EtherChannel | shared control plane; upgrades usually reload the whole stack |
| **MLAG/vPC** pair | two control planes, active-active L2 uplinks, no STP blocking | vendor-specific, peer-link and split-brain handling to get right |
| **Routed access + ECMP** | no STP, fast deterministic convergence, scales | VLANs cannot span access switches; needs L3 at the edge |
| Classic STP | works everywhere | half the links blocked; 1–6 s convergence with RSTP, longer with legacy STP |
Prefer routed (L3) designs where VLANs do not need to stretch; keep L2 domains small.

## 5. Convergence budget
Failover time = detection + propagation + recomputation + forwarding update.
- Detection dominates. Link-down on directly connected fibre is fast (ms); a failure
  behind a media converter, carrier Ethernet or a transparent device is not seen and
  waits for protocol dead timers (OSPF 40 s, BGP 180 s by default).
- **BFD** gives sub-second detection for OSPF, BGP and static routes; e.g. 300 ms × 3.
  Check hardware offload support before going aggressive.
- Dual ISPs with BGP: failover inbound depends on the internet re-converging (tens of
  seconds to minutes). Without BGP (two ISPs, two address blocks) inbound failover is
  DNS-based and depends on TTLs.

## 6. Capacity under failure
Redundant links must each carry the full load when the other fails. Two 10G uplinks
running at 70% each are a 14G load on one 10G link after failure: you have a congestion
outage instead of a link outage. Plan N+1 at ≤ 50% per link in active-active pairs.

## 7. Prove it
- Write a failover test plan per component: action (pull cable, power off, shut BGP),
  expected result, measured interruption (continuous `ping -i 0.2` or a traffic generator,
  plus an application-level check).
- Run it at commissioning and after major changes, in a maintenance window, with a
  rollback ready. Record measured times against the requirement.
- Monitor the standby path: a backup link that has been down for months is found only
  when you need it.

## Verify
- [ ] Outage tolerance written per service; design maths matches it.
- [ ] Shared-fate review done for physical route, power, control plane, config and provider.
- [ ] Gateways use VRRP/HSRP with preempt delay and uplink tracking.
- [ ] Any surviving path can carry full load.
- [ ] Every redundant component failed on purpose; measured failover time recorded.
- [ ] Standby paths are monitored and alarmed.
