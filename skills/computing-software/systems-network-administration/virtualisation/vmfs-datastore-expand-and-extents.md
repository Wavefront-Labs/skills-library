---
id: computing-software.systems-network-administration.virtualisation.vmfs-datastore-expand-and-extents
name: vmfs-datastore-expand-and-extents
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmfs-extent, datastore-expand, vmfs, datastore, vsphere-storage, vmkfstools, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Grow a VMFS datastore after the array LUN is enlarged: rescan, Increase Datastore Capacity in place, CLI fallback with partedUtil and vmkfstools, and why to avoid extents."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-storage-8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Increase VMFS datastore capacity

## Preferred: grow the same LUN
1. Grow the LUN on the array.
2. Rescan HBAs on **all** hosts (Cluster → Storage → Rescan Storage, or
   `esxcli storage core adapter rescan --all`).
3. Datastore → Increase Datastore Capacity → choose the **same device** (shows
   "Expandable: Yes") → use "all available partitions" free space.

Online, no VM downtime.

## CLI fallback (wizard fails or device shows wrong size)
Follow the datastore-expansion CLI procedure in the vSphere Storage documentation
(vmkfstools filesystem-growth options): extend the partition, then grow the VMFS
filesystem. Run it on one host, then rescan the others.

## Extents (adding a second LUN)
Datastore → Increase → choose a *different* device spans the volume. Avoid: losing any
extent LUN takes the whole datastore offline, troubleshooting is harder, and you cannot
remove an extent without deleting the datastore. Use only as an emergency; plan Storage
vMotion to a single larger LUN afterwards.

## Gotchas
- If the new size does not appear, the array may need a host-side rescan twice, or the
  LUN is presented with different sizes to different hosts (check
  `esxcli storage core device list -d naa...` Size on each host).
- Thin-on-thin: growing the datastore increases overcommit headroom; check the array pool
  has physical capacity.
- Datastores on vSAN/NFS/vVols are not grown this way (policy/export/array side).

## Verify
Capacity updated on every host (`df -h` in ESXi shell), no extent added unintentionally
(Datastore → Configure → Device Backing shows one device).

## Checked
2026-10-31: Confirmed `esxcli storage core adapter rescan` and the rescan-all form against
the ESXCLI storage reference page, and the RDM/VMFS mapping context against the vmkfstools
documentation. Replaced the unconfirmed partedUtil/vmkfstools --growfs command block with a
pointer to the documented expansion procedure and removed the 64 TB VMFS6 maximum.
Method: documentation only; no commands were run.
