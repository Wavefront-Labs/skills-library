---
id: computing-software.systems-network-administration.virtualisation.vds-lacp-link-aggregation
name: vds-lacp-link-aggregation
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vds-lacp, link-aggregation-group, lacp, lag, distributed-switch, vsphere-networking, port-channel, vmware, esxi, vsphere]
level: advanced
status: draft
description: "Configure LACP LAGs on a vSphere Distributed Switch: LAG mode and hash, the standby-to-active migration sequence, switch side settings and when LACP is not worth it."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking-8-0.html
  - https://knowledge.broadcom.com/external/article?legacyId=2051307
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LACP link aggregation groups on a vDS

**Goal:** dynamic link aggregation that the physical switch negotiates, configured
without dropping the host mid-migration.

## Should you?
LACP adds a dependency on switch config for limited gain: a single flow still uses one
link. Load-based teaming on plain trunks gives most of the benefit with less risk.
Use LACP when the network team mandates port channels everywhere or a single VM needs
multi-link throughput across many flows. Not supported for iSCSI port binding vmks or
with vSAN in some topologies; check the guide.

## Configure
1. vDS → Configure → LACP → **New LAG**: name, number of ports (= uplinks per host),
   mode **Active** (one side must be active), load balancing hash matching the switch
   (e.g. source and destination IP, TCP/UDP port).
2. Physical switch: an LACP port channel per host (`channel-group N mode active`),
   trunk with the same allowed VLANs, across a stack or MLAG/vPC pair.
3. Distributed port groups → Teaming and failover: move the LAG to **Standby**, keep
   current uplinks Active (intermediate state; the client warns, that is expected).
4. Add/Manage Hosts → assign physical NICs to LAG ports, one at a time if you only have
   two NICs, checking connectivity after each.
5. Port groups: LAG to **Active**, standalone uplinks to **Unused**. Teaming policy is
   taken from the LAG hash.

## Diagnose
```sh
esxcli network vswitch dvs vmware lacp status get
esxcli network vswitch dvs vmware lacp config get
```
Look for partner system ID and `Bundled` state on each NIC. On the switch:
`show etherchannel summary` (Cisco) shows `(P)` bundled vs `(I)`/`(s)` stand-alone or
suspended.

## Failure modes
- Switch side configured as static (mode on) while the LAG is LACP: ports suspend.
- Moving the last management uplink into the LAG before the switch side is up isolates
  the host; network rollback normally reverts it, DCUI Restore Standard Switch if not.
- Mixing NIC speeds in a LAG: the slower link gets suspended.

## Verify
All host NICs show Bundled with the same partner ID; pulling one cable does not drop
VM pings; `show lacp neighbor` on the switch lists every host NIC.
