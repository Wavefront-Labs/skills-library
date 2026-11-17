---
id: computing-software.systems-network-administration.cisco-networking.stp-root-guard-and-loop-guard
name: stp-root-guard-and-loop-guard
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, spanning-tree, stp, root-guard, loop-guard, root-inconsistent, loop-inconsistent, udld, bpdu-guard]
level: practitioner
status: docs-checked
description: "Where STP root guard and loop guard go on Catalyst IOS switches, the commands, syslog messages, inconsistent states, and how loop guard differs from UDLD and BPDU guard."
sources:
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/10588-74.html
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol-stp-8021d/218321-configure-stp-with-loop-guard-and-bpdu-s.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Root guard and loop guard

Based on two Cisco support documents for Catalyst IOS switches: "Enhance Spanning Tree Protocol (STP) with Root Guard" (10588) and "Configure STP with Loop Guard and BPDU Skew Detection" (218321, formerly 10596). Both are written for Catalyst IOS generally; check that your platform and release support the feature.

## Where each goes
| Feature | Port role | Effect |
|---|---|---|
| Root guard | ports where the root bridge must not appear (toward access or other administrative domains) | port stays designated; a superior BPDU puts it in root-inconsistent state |
| Loop guard | non-designated ports (root and alternate ports) in all possible topologies | stops a port that stops receiving BPDUs from becoming designated |
| BPDU guard | PortFast ports | disables the port on BPDU receipt |

## Root guard
```
interface fastethernet 3/1
 spanning-tree guard root
```
- On newer Catalyst IOS the command is `spanning-tree guard root`; on 2900XL/3500XL/2950/3550 it was `spanning-tree rootguard` (and for Catalyst 6500 it changed from `rootguard` to `guard root` in 12.1(3a)E3).
- Root guard keeps the port designated. When a superior BPDU arrives, the port goes to root-inconsistent, which is effectively equal to listening: no traffic is forwarded. When the superior BPDUs stop, the port recovers on its own through listening and learning to forwarding.
- Log message in the document: `%SPANTREE-2-ROOTGUARDBLOCK: Port 1/1 tried to become non-designated in VLAN 77. Moved to root-inconsistent state`.
- Setting bridge priority 0 does not guarantee root position (a lower MAC address with priority 0 still wins), which is why root guard exists.
- Root guard does not fix the two-roots problem caused by a unidirectional link; UDLD and loop guard address that.

## Loop guard
```
interface gigabitEthernet 1/1
 spanning-tree guard loop        ! per port; disabled by default
spanning-tree loopguard default  ! global
```
- `no spanning-tree guard loop` disables it on an interface and `no spanning-tree loopguard default` globally.
- If a non-designated port stops receiving BPDUs it goes to loop-inconsistent (effectively blocking) instead of becoming designated and forwarding. The state is per VLAN; on an EtherChannel the whole channel is blocked for that VLAN.
- Recovery is automatic when a BPDU is received. Messages: `%SPANTREE-2-LOOPGUARD_BLOCK: Loop guard blocking port FastEthernet0/24 on VLAN0050.` and `%SPANTREE-2-LOOPGUARD_UNBLOCK: Loop guard unblocking port FastEthernet0/24 on VLAN0050.`
- The global form enables loop guard on all point-to-point links, detected by full duplex; per-port settings can override it.
- Restrictions in the document: not on PortFast ports or dynamic VLAN ports, not on shared links, and mutually exclusive with root guard (configuring loop guard disables root guard on that port). It functions correctly with MST. UplinkFast and BackboneFast are transparent to it.
- Verify with `show spanning-tree summary` (the line `Loopguard Default is enabled`).

## Loop guard versus UDLD
| | Loop guard | UDLD |
|---|---|---|
| Action granularity | per VLAN | per port |
| Protects against unidirectional-link STP failures | yes, when on all root and alternate ports | yes, when on all links |
| Protects against designated switch not sending BPDUs (software problem) | yes | no |
| Protects against incorrect wiring | no | yes |
| Link unidirectional since link-up | not covered | covered |

On an EtherChannel with one bad link, UDLD disables only the failed link while loop guard blocks the whole channel for the VLAN. The document says the highest protection comes from enabling both.

## BPDU guard versus root guard
BPDU guard disables a PortFast port on BPDU reception; re-enable manually or with the errdisable timeout. Root guard allows the device to take part in STP as long as it does not try to become root, and recovers automatically.

## Checked
Date: 2026-11-08. Read end to end: Cisco document 10588 "Enhance Spanning Tree Protocol (STP) with Root Guard" (rev 5.0, June 2026) and Cisco "Configure STP with Loop Guard and BPDU Skew Detection" (the old 10596-84 URL redirects to 218321, which replaces it in sources), both fetched with tools/review/fetch_pages.py.
Corrected: root guard syslog is `%SPANTREE-2-ROOTGUARDBLOCK` (no underscore before BLOCK); loop guard global applies to point-to-point (full-duplex) links, not "non-edge ports".
Removed because neither page confirms them: the UDLD aggressive/normal commands and `%UDLD-4-UDLD_PORT_DISABLED`, the whole BPDU filter section and its global form, `show spanning-tree inconsistentports`, `show udld neighbors`, `show spanning-tree interface detail`, the `bridge assurance` tag, and the `show run | i bpdufilter` check.
Method: documentation only; no commands were run.
