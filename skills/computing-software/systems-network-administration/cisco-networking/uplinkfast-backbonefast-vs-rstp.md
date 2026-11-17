---
id: computing-software.systems-network-administration.cisco-networking.uplinkfast-backbonefast-vs-rstp
name: uplinkfast-backbonefast-vs-rstp
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, spanning-tree, uplinkfast, backbonefast, rstp, rapid-pvst, stp-convergence, legacy-stp]
level: practitioner
status: docs-checked
description: "Understand legacy UplinkFast and BackboneFast, why RSTP (802.1w) builds in the same behaviour, and what to expect when moving an 802.1D estate to Rapid PVST+."
sources:
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/10575-51.html
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/24062-146.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UplinkFast and BackboneFast vs RSTP

## What UplinkFast did for 802.1D
- Cisco-proprietary; recovers from the failure of a directly connected uplink in about a second, against about 30 s
  with default 802.1D timers (the document gives 14 s with aggressive timer tuning).
- Works only on a switch with a non-self-looped blocked port, so use it on access switches with redundant uplinks,
  not on distribution or core switches. It is enabled for the whole switch, not per VLAN.
- The uplink group is the root port plus the blocked ports that lead to the root. When the root port fails, the next
  lowest cost port in the group goes straight to forwarding.
- The switch floods dummy multicast frames sourced from the MACs in its CAM table so upstream CAMs relearn; the
  rate is configurable.
- Enabling it raises the bridge priority (49152 in the IOS example) and adds 3000 to port costs so the switch is
  unlikely to become root or a designated port. Do not change the spanning-tree priority while it is enabled: on some
  platforms that disables it or causes a loop.
- The old root port is held blocked for about 35 s (2 x forward_delay + 5 s) after it returns before UplinkFast
  switches back, to protect against a flapping link.
- It reacts only to a direct link failure; BackboneFast covers indirect failures.
- IOS commands in the document: `spanning-tree uplinkfast`, `no spanning-tree uplinkfast` (on IOS the cost and
  priority revert automatically; on CatOS `clear spantree uplinkfast` is needed), `show spanning-tree`.

## Why RSTP replaces them
- UplinkFast: when a bridge loses its root port, RSTP puts its best alternate port directly into forwarding; the
  topology change clears CAM entries upstream, so the dummy-multicast process is not needed. No further
  configuration; it is enabled automatically.
- BackboneFast: the document calls "accepts inferior BPDUs" the core of the BackboneFast engine and says 802.1w
  incorporated a similar mechanism: a bridge that receives inferior information from its designated or root bridge
  accepts it immediately.
- Edge ports play the role of PortFast; a misconfigured edge port can lose connectivity when a link to the root
  comes up.
- RSTP BPDUs are type 2, version 2, so legacy bridges drop them and RSTP detects legacy neighbours.

## Migration cautions
- Rapid transitions need point-to-point links (full-duplex unless explicitly configured); otherwise the port falls
  back to the 802.1D listening-learning sequence, as it does when the neighbour does not understand RSTP.
- RSTP interoperates with legacy STP per port, but the fast-convergence benefits are lost on ports facing legacy
  bridges.
- Look up the platform's Spanning Tree chapter for the exact mode and PortFast commands and for whether
  UplinkFast/BackboneFast are accepted in rapid-pvst mode; the two documents cited here do not say.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read document 10575 (UplinkFast) in full (background, theory,
changes implied, limitations, IOS and CatOS configuration, conclusion) and document 24062 (RSTP) at the UplinkFast,
accepts-inferior-BPDUs, point-to-point, edge-port and legacy-compatibility sections (found by search plus reading
around the hits, not end to end). Confirmed: about one second vs 30 s, 14 s tuned, priority 49152 and +3000 cost in
the IOS output, 35 s hold (2 x forward_delay + 5), the IOS commands, whole-switch scope. Removed as unconfirmed by
these pages: the "~1-5 s" and "30 s vs 50 s" BackboneFast figures, RLQ and the max-age skip, the claim that
uplinkfast/backbonefast commands are accepted but ignored under rapid-pvst, the migration command listing
(`spanning-tree mode rapid-pvst`, `portfast default`, `link-type`, `show spanning-tree summary`) and the invented
Verify steps (sub-second pull test).
