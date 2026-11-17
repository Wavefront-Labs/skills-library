---
id: computing-software.systems-network-administration.virtualisation.esxi-path-selection-policy-nmp-hpp
name: esxi-path-selection-policy-nmp-hpp
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [path-selection-policy, nmp, hpp, satp, psp, round-robin, vmw-psp-rr, claim-rules, multipathing, vsphere-storage, vmware, esxi, vsphere]
level: advanced
status: docs-checked
description: "Manage ESXi multipathing: NMP SATP/PSP, Round Robin with IOPS=1 via claim rules, HPP for NVMe, ALUA states and finding dead or standby paths with esxcli."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=2069356
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ESXi path selection: NMP, SATP, PSP and HPP

**Goal:** every LUN uses the array vendor's recommended policy on every host, set by rule
so new LUNs inherit it.

## Layers
- **PSA** (pluggable storage architecture) claims devices for a multipathing plugin.
- **NMP** (native) uses a **SATP** (array-type plugin, e.g. `VMW_SATP_ALUA`) and a **PSP**:
  `VMW_PSP_FIXED`, `VMW_PSP_MRU`, `VMW_PSP_RR` (round robin).
- **HPP** (high-performance plugin) handles NVMe devices; see the vSphere Storage
  documentation for its current scope and path schemes.

## Inspect
```sh
esxcli storage nmp device list                 # SATP, PSP, working paths per device
esxcli storage core path list -d naa.<id>      # state: active, standby, dead
esxcli storage nmp satp rule list | grep -i <vendor>
esxcli storage hpp device list
```
ALUA arrays report paths as **Active (I/O)** (optimised) vs **Active** (non-optimised):
I/O should go only to optimised paths. Seeing I/O on non-optimised paths means the array
is in the wrong ALUA mode or a controller failed over.

## Set policy by claim rule (preferred)
```sh
# Example: vendor recommends RR with path switch every I/O
esxcli storage nmp satp rule add -s VMW_SATP_ALUA -V "<VENDOR>" -M "<MODEL>" \
   -P VMW_PSP_RR -O "iops=1" -c tpgs_on -e "vendor RR rule"
```
New LUNs pick this up; existing LUNs need a reclaim (unmount/reboot) or a per-device set:
```sh
esxcli storage nmp device set -d naa.<id> -P VMW_PSP_RR
esxcli storage nmp psp roundrobin deviceconfig set -d naa.<id> -t iops -I 1
```
Many arrays ship rules already in recent ESXi builds; check before adding duplicates.

## Gotchas
- **MRU vs Fixed:** Fixed on an active/passive array can cause path thrashing between
  controllers; follow the vendor.
- Round Robin with default IOPS=1000 underuses paths on fast arrays; vendors often say 1.
- Mismatched policy between hosts sharing a LUN can trigger LUN trespass on A/P arrays.
- Dead paths that are never cleaned up mask real failures; investigate, don't ignore.

## Verify
`esxcli storage nmp device list` shows the intended PSP on every shared LUN on every host;
each LUN has the expected number of active paths.

## Checked
2026-10-31: `VMW_PSP_FIXED`/`VMW_PSP_MRU`/`VMW_PSP_RR`, `VMW_SATP_ALUA`, `esxcli storage nmp satp rule list`, `esxcli storage nmp psp roundrobin deviceconfig set`, the default Round Robin IOPS limit of 1000 and the `tpgs_on` claim-rule options confirmed in KB 2069356. Removed unconfirmed specifics: the HPP path scheme names and the PowerCLI cluster-view example.
Method: documentation only; no commands were run.
