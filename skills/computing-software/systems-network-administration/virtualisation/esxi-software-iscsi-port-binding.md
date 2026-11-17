---
id: computing-software.systems-network-administration.virtualisation.esxi-software-iscsi-port-binding
name: esxi-software-iscsi-port-binding
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-iscsi, iscsi-port-binding, software-iscsi, vmkernel-adapter, dynamic-discovery, chap, vsphere-storage, multipathing, vmware, esxi, vsphere]
level: practitioner
status: docs-checked
description: "Configure the ESXi software iSCSI adapter: one vmk per NIC with port binding, when not to bind (routed targets), discovery, CHAP, delayed ACK and path checks."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=2038869
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ESXi software iSCSI with port binding

**Goal:** every LUN reachable over multiple independent paths, with failover handled by
ESXi multipathing rather than NIC teaming.

## Port binding or not?
- **Bind** when the target portals are on the **same subnet/L2** as the iSCSI vmks and
  the array presents a single portal (most single-subnet arrays).
- **Do not bind** when targets are on different subnets reached through a router, or the
  array uses multiple subnets (one vmk per subnet, routing decides). Binding with routed
  targets causes path flapping and long rescans.

## Configure (bound design)
1. vSwitch or vDS with two uplinks; two port groups, iSCSI-A (vmnic2 active, vmnic3
   **unused**), iSCSI-B (the reverse). Exactly one active uplink, no standby.
2. vmk1/vmk2 on those port groups, MTU 9000 if the whole path supports it.
3. Enable the software adapter and bind:
```sh
esxcli iscsi software set --enabled=true
esxcli iscsi adapter list                                   # e.g. vmhba64
esxcli iscsi networkportal add -A vmhba64 -n vmk1
esxcli iscsi networkportal add -A vmhba64 -n vmk2
esxcli iscsi adapter discovery sendtarget add -A vmhba64 -a <portal-ip>:3260
esxcli iscsi adapter auth chap set -A vmhba64 --direction=uni --level=required --authname=<iqn-or-name> --secret=<secret>
esxcli storage core adapter rescan -A vmhba64
```
4. Set the path selection policy per the array vendor (often Round Robin, IOPS=1).

## Tuning and gotchas
- **Delayed ACK**: some arrays recommend disabling it (adapter Advanced Options) to avoid
  latency spikes; follow the vendor doc, not habit.
- Login timeout / NoopOut settings are vendor-guided too.
- Static discovery is useful when you must avoid every host logging into every target.
- Keep iSCSI on dedicated VLANs and physical NICs where possible; don't route iSCSI.
- Changing port binding requires a rescan and can cause brief APD on bound paths; do it
  in maintenance mode.

## Verify
```sh
esxcli iscsi session list -A vmhba64          # one session per vmk per target
esxcli storage core path list | grep -E "Runtime Name|State"
vmkping -I vmk1 -d -s 8972 <portal-ip>
```
Each LUN should show N paths (vmks x portals), all `active`; disable one uplink and I/O
continues.

## Checked
2026-10-31: Confirmed when to use and when not to use port binding (same subnet/broadcast
domain and vSwitch, one-to-one vmk-to-vmnic mapping, no LACP, no port binding with routed
different-subnet targets) against Broadcom KB 317719 (legacyId 2038869), and the esxcli
iscsi software/adapter/networkportal/discovery/chap commands against the ESXCLI iscsi
reference page. No claim changes were needed.
Method: documentation only; no commands were run.
