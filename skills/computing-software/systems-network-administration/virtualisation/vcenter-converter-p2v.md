---
id: computing-software.systems-network-administration.virtualisation.vcenter-converter-p2v
name: vcenter-converter-p2v
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vcenter-converter, p2v, v2v, vmware, vsphere]
level: practitioner
status: draft
description: "Convert physical or other-hypervisor machines to vSphere VMs with VMware vCenter Converter Standalone: ports, source agent, volume options, sync and cutover."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vcenter-converter-standalone.html
  - https://vinfrastructure.it/2025/09/vmware-standalone-converter-guest-os-support-2025/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# P2V with vCenter Converter Standalone

**Goal:** move a physical server (or a VM from another platform) into vSphere with minimal downtime.

## Availability
Converter Standalone was withdrawn from download in 2022 and Broadcom re-released it as 9.0 (August 2025, build 24908347 per third-party coverage; adds VCF 9.0 and hardware version 22 support, SSL certificate verification, and synchronisation for Linux sources). Download the current build from the Broadcom support portal; whether a release newer than 9.0 exists was not confirmed. Avoid old 6.x builds with known security issues.

## Ports (unconfirmed against the current KB; check Broadcom's Converter port list)
| From -> To | Port |
|---|---|
| Converter server -> powered-on Windows source | TCP 445, 139, 9089 (agent) |
| Converter server -> Linux source | TCP 22 |
| Converter server -> vCenter | TCP 443 |
| Source machine -> ESXi host | TCP 443, 902 (data copy) |
Name resolution of the ESXi host from the source is required.

## Conversion job
1. *Convert machine*: source powered-on (remote Windows/Linux, or local), destination vCenter, target host/datastore, VM name, hardware version.
2. **Data to copy**: select volumes, resize them, choose thin provisioning; *volume-based block-level* is fastest when not resizing smaller.
3. **Devices**: vCPU, memory, SCSI controller type (LSI SAS/PVSCSI), NICs and port groups (start disconnected).
4. **Services**: stop application services at the final sync; set services on the destination (disabled until checked).
5. **Advanced**: *Synchronize changes* (Windows; Linux sources too from 9.0) for an incremental final pass; *Power off source* and *Power on destination* at completion; *Install VMware Tools*; *Remove System Restore checkpoints*.

## Cutover
Initial copy online, then a short window: stop apps, run the sync, power off source, connect destination NIC, start, test. Keep the physical box powered off but intact until sign-off.

## Post-conversion
Remove vendor hardware agents and drivers, hidden ghost NICs (re-enter IP on the new adapter), disable unnecessary services, check disk alignment and time sync settings.

## Gotchas
- Linux sources: the helper VM needs a static IP reachable from the source over SSH; LVM and software RAID are converted to basic volumes.
- Domain controllers and databases: prefer rebuild/migration methods over P2V where possible.
