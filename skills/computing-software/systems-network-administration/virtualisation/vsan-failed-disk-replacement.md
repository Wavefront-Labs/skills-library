---
id: computing-software.systems-network-administration.virtualisation.vsan-failed-disk-replacement
name: vsan-failed-disk-replacement
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsan-disk-replacement, vsan, vsan-osa, vsan-esa, disk-group, esxcli-vsan, vmware, vsphere]
level: advanced
status: draft
description: "Replace a failed vSAN cache or capacity device on OSA and ESA: identify the disk, check resync and data accessibility, remove, swap, claim, and verify rebuild."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsan/vsan/8-0.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Replacing a failed vSAN device

## Identify
Cluster → Configure → vSAN → Disk Management: device shows "Permanent disk failure" or
"Absent". On the host:
```sh
esxcli vsan storage list | egrep "Device|Is Capacity Tier|In CMMDS|Health"
esxcli vsan debug disk list            # health per disk
esxcli storage core device set -d naa.xxx -l=locator -L=120   # blink LED (if supported)
```

## Know what failure removes
| Architecture | Device | Impact |
|---|---|---|
| OSA | **Cache** SSD | the whole disk group goes offline |
| OSA | Capacity device (dedup/compression **on**) | whole disk group offline |
| OSA | Capacity device (dedup off) | that device only |
| ESA | any device | that device only (single tier, no disk groups) |

## Steps
1. Check resync and objects: Monitor → vSAN → Resyncing Objects; Skyline Health "Data"
   section. If failed components are already rebuilt elsewhere (repair delay 60 min
   passed for absent; immediate for degraded), objects are compliant.
2. Remove the device (or disk group) in Disk Management with data migration
   **"No data migration"** if it is already dead, otherwise **"Ensure accessibility"**/
   **"Full data migration"** for a healthy-but-suspect disk.
3. Physically replace (hot-swap if the controller supports; verify passthrough/HBA mode).
4. Rescan, confirm the new device is visible and has no partitions
   (`partedUtil getptbl /vmfs/devices/disks/naa.new`; wipe stale partitions from the
   UI "Erase partitions" if reused).
5. Claim: OSA → add to existing disk group (capacity) or recreate disk group (cache);
   ESA → Claim unused disks to vSAN storage pool.

## Gotchas
- Replacement must be on the vSAN HCL for the same controller and firmware; mismatched
  firmware triggers health warnings and possible data errors.
- Do not reboot a host with a failed cache device hoping it comes back; it can mark
  more components absent and start a bigger rebuild.
- Small clusters (3 nodes, FTT=1) have no spare fault domain: objects stay reduced
  redundancy until the disk is back.

## Verify
Disk Management shows device healthy and in CMMDS; Resyncing Objects drains to 0; vSAN
object health all "Healthy"; capacity restored.
