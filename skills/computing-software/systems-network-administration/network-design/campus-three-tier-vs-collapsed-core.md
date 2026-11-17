---
id: computing-software.systems-network-administration.network-design.campus-three-tier-vs-collapsed-core
name: campus-three-tier-vs-collapsed-core
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-topology, campus-design, three-tier, hierarchical-design, collapsed-core, two-tier, access-layer, distribution-layer, core-layer, routed-access, soho, small-branch, failure-domain]
level: practitioner
status: docs-checked
description: "Choose a campus architecture: three-tier core/distribution/access vs collapsed core vs single-switch SOHO/branch, sizing rules, where L2 ends, and failure-domain reasoning."
sources:
  - https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-campus-lan-wlan-design-guide.html
  - https://learningnetwork.cisco.com/s/ccna-exam-topics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Campus topology: three-tier, collapsed core, small branch

## Layers and jobs
| Layer | Job | Typical features |
|---|---|---|
| Access | connect endpoints | PoE, 802.1X, port security, QoS marking, voice VLAN |
| Distribution | aggregate access closets, policy boundary, L2/L3 demarcation | FHRP or L3 gateways, summarisation, ACLs |
| Core | fast transport between distribution blocks, DC, WAN edge | routed only, no policy, high bandwidth, redundancy |

## Choosing
| Design | When | Notes |
|---|---|---|
| Three-tier | large campus with several distribution blocks | a core avoids full-mesh links between distribution blocks |
| Collapsed core (two-tier) | one building or a small campus, a few closets | core and distribution in one redundant pair (stack, StackWise Virtual, MLAG/vPC) |
| SOHO / small branch | small site | one router/firewall + one switch stack + APs; often SD-WAN appliance with integrated switching |
Cisco notes the core can be collapsed into the two distribution switches in a small campus (collapsed distribution and core).

## Where Layer 2 ends
- **Traditional**: L2 from access to distribution (VLANs per closet, STP, FHRP at distribution).
  Keep VLANs local to one closet: no VLAN spanning the campus.
- **Routed access**: L3 at the access switch (each closet routes, /31 uplinks, OSPF/EIGRP),
  no STP between layers, fast ECMP convergence; costs: an IP subnet per closet, L3 licences.
- **Fabric** (SD-Access, EVPN): L2 extension over an L3 underlay when mobility needs it.

## Failure domains
- A broadcast storm or STP loop affects one VLAN everywhere that VLAN exists: keep VLANs small
  and local.
- Pair every distribution/core function (two boxes, or a stack with separate power), dual-home
  every access switch with two uplinks to two distribution members (EtherChannel to a stack/MLAG).
- Separate management (OOB) so a data-plane failure still allows access.

## Sizing checks
Cisco cites uplink ratios up to 20:1 access to distribution and 4:1 distribution to core as implemented (see spine-leaf-and-oversubscription). Size PoE budgets per closet (see poe-standards-and-power-budget).

## Verify
- [ ] Diagram shows each layer with redundancy, and no VLAN spanning more than one closet (unless designed fabric).
- [ ] Single device or link failure test causes no loss of reachability beyond convergence time.

## Checked

- Date: 2026-10-28
- Confirmed: Cisco campus overview: three-tier core/distribution/access model and the collapsed distribution-and-core option; design guide: 20:1 and 4:1 uplink ratios.
- Removed: distribution-block and user-count thresholds, the separate-core rule of thumb.
Method: documentation only; no commands were run.
