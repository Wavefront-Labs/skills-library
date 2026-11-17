---
id: computing-software.systems-network-administration.virtualisation.datastore-unmount-and-lun-detach
name: datastore-unmount-and-lun-detach
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [datastore-unmount, lun-detach, vsphere-storage, vmfs, pdl, esxcli, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Decommission a VMFS datastore or LUN without causing APD: evacuate, unmount, detach on every host, unpresent at the array, then rescan and clean up."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-storage-8-0.html
  - https://developer.broadcom.com/xapis/esxcli-command-reference/latest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unmount a datastore and detach the LUN

Unpresenting a LUN at the array while hosts still have it attached produces an
**All Paths Down** condition: hostd threads block, hosts can go "not responding". The
order below avoids that.

## Pre-checks (datastore must be idle)
- No VMs, templates, ISOs, or snapshot deltas on it (Datastore → VMs, and search
  `*.vmdk` for disks of VMs living elsewhere).
- Not an HA heartbeat datastore (Cluster → vSphere HA → Heartbeat Datastores).
- Not in a datastore cluster with SDRS, not the scratch location, not a coredump file target, not holding
  vSphere Cluster Services (vCLS) VMs (use retreat mode or SDRS will move them back).
- SIOC disabled on it.
The unmount wizard runs these checks per host; read every red X.

## Steps
1. **Unmount** (all hosts): Datastore → Unmount Datastore → select all hosts.
   ```sh
   esxcli storage filesystem unmount -l DS_OLD
   ```
2. **Detach** the device on every host (Storage Devices → Detach), get the NAA id first:
   ```sh
   esxcli storage vmfs extent list | grep DS_OLD        # naa.600...
   esxcli storage core device set --state=off -d naa.600xxxx
   esxcli storage core device detached list
   ```
3. **Unpresent** at the array (remove from host group / igroup / zoning).
4. **Rescan** all hosts: `esxcli storage core adapter rescan --all`.
5. **Clean** the detached list so the device does not reappear in config:
   `esxcli storage core device detached remove -d naa.600xxxx`

## Gotchas
- Doing step 3 before step 2 on any single host is the classic APD cause.
- A device in "PDL" state after unpresent (sense code 0x5 0x25) is handled; APD is not.
- Shared RDMs on the LUN: remove from VMs first or detach fails with "device busy".
- For NFS, just unmount on all hosts (`esxcli storage nfs remove -v DS_NFS`).

## Verify
`esxcli storage core device list -d naa.600xxxx` returns not found on every host after
cleanup; no APD events in `/var/log/vmkernel.log`; hosts stay connected.

## Checked
2026-10-31: Confirmed `esxcli storage filesystem unmount`, `esxcli storage vmfs extent
list`, `esxcli storage core device set --state=off`, `detached list` and `detached remove`
against the ESXCLI storage reference page. Removed the ScratchConfig setting name.
Method: documentation only; no commands were run.
