---
id: computing-software.systems-network-administration.cisco-networking.ospf-spf-throttle-and-bfd
name: ospf-spf-throttle-and-bfd
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ospf, spf-throttle, lsa-throttle, bfd, convergence, timers]
level: practitioner
status: docs-checked
description: "Tune OSPF convergence: BFD for detection, SPF and LSA throttle timers for calculation and flooding, LSA arrival, and how to measure convergence before and after."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/command/iro-cr-book/ospf-s1.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/command/iro-cr-book/ospf-a1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPF fast convergence: SPF throttling and BFD

Convergence = detect + flood + compute + install. Each has a knob.

## 1. Detect: BFD
```
interface Gi0/1
 bfd interval 50 min_rx 50 multiplier 3
router ospf 1
 bfd all-interfaces
show bfd neighbors
```

## 2. Generate and flood: LSA throttle
```
router ospf 1
 timers throttle lsa all 0 20 5000     ! start hold max (ms)
 timers lsa arrival 15                 ! minimum ms between acceptance of the same LSA
```
The first instance of an LSA is always generated immediately on a local topology change; later
instances wait according to the hold and max intervals. `timers lsa arrival` sets the minimum
interval at which the router accepts the same LSA from a neighbour (range 0 to 600,000 ms, default
1000 ms), so keep it consistent with the neighbours' throttle settings or you discard legitimate
updates.

## 3. Compute: SPF throttle
```
router ospf 1
 timers throttle spf 50 200 5000      ! spf-start, spf-hold, spf-max-wait (ms)
```
`spf-start` is the initial delay before an SPF run after a change, `spf-hold` the minimum hold time
between two consecutive runs, and `spf-max-wait` the maximum wait; each ranges from 1 to 600000 ms.
Look up the default for your platform and release before changing it.

## Check and measure
```
show ip ospf
show ip ospf statistics
```
Measure with a continuous ping at 10 ms intervals across the network while you shut a link; lost
packets x 10 ms = outage. Compare before and after.

## Gotchas
- Aggressive timers on CPU-starved routers cause flaps that throttling then masks.
- Make settings consistent across the area; one slow router delays everyone's forwarding
  correctness (microloops).

## Verify
- [ ] Measured failover under your target for a link failure.
- [ ] `show ip ospf statistics` shows SPF runs starting within the configured initial wait.

## Checked
2026-10-31. Confirmed in the Cisco OSPF command reference (`timers throttle spf` arguments and
1 to 600000 ms range; `timers throttle lsa all` start/hold/max, first LSA generated immediately;
`timers lsa arrival` range and 1000 ms default; `show ip ospf statistics`; `bfd all-interfaces`) and
the BGP reference for the BFD interval syntax. Removed: the "5000/10000/10000" default claim
(documented there only for OSPF for IPv6), `ip ospf bfd`, exponential back-off wording, the
`prefix-priority high route-map` section (the reference shows `prefix-priority` only under
fast-reroute), the iSPF remark and the hardware-offload remark.
Method: documentation only; no commands were run.
