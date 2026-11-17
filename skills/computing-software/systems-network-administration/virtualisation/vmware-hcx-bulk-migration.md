---
id: computing-software.systems-network-administration.virtualisation.vmware-hcx-bulk-migration
name: vmware-hcx-bulk-migration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hcx, hcx-bulk-migration, vmotion, migration, vmware, vsphere]
level: advanced
status: draft
description: "Plan and run VMware HCX bulk migrations: service mesh, migration types, switchover windows, seed checkpoints and common failure causes."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/hcx/vmware-hcx/4-10/vmware-hcx-user-guide-4-10.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/hcx/vmware-hcx/4-10/vmware-hcx-user-guide-4-10/migrating-virtual-machines-with-vmware-hcx.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bulk migration with VMware HCX

**Goal:** move many VMs between vSphere sites (on-prem to on-prem, or to VMware Cloud) with a controlled cutover window.

## Building blocks
- **HCX Connector** at the source, **HCX Cloud Manager** at the destination; pair them with a *Site Pair*.
- **Compute profile** (clusters, datastores, service networks) and **network profiles** (management, uplink, vMotion, replication) on each side.
- **Service mesh** deploys the appliances: Interconnect (IX), Network Extension (NE), optional WAN Optimization.
- Firewalls: TCP 443 to managers, UDP 4500 between IX/NE uplinks (IPsec).

## Migration types
| Type | Downtime | Use |
|---|---|---|
| Bulk Migration | One reboot at switchover | Many VMs in parallel, scheduled |
| HCX vMotion | None | Few VMs, serial |
| Replication Assisted vMotion (RAV) | None | Many VMs in parallel with live switchover |
| Cold Migration | Powered off | Templates, off VMs |
| OS Assisted Migration | Reboot | Non-vSphere (KVM, Hyper-V) sources |

## Running bulk migration
1. Migration -> New -> select VMs into a *mobility group*.
2. Set destination folder, resource pool, datastore, disk format, and network mapping (to extended or routed networks).
3. Schedule a **switchover window**; replication starts immediately and switchover runs in the window.
4. Options: *Retain MAC*, *Upgrade VMware Tools*, *Upgrade virtual hardware*, *Remove snapshots*, *Force unmount ISO*, *Seed checkpoint* (reuse already-replicated data if you retry).
5. Validate, then Go. The source VM is powered off and renamed with a `POSTMIGRATE` suffix, not deleted; keep it until sign-off.

## Common failures
- Mounted ISOs or snapshots block replication; tick the cleanup options.
- Service mesh tunnel down: check UDP 4500 and MTU on the uplink path (diagnostics in the mesh view).
- RDMs and shared disks are not supported; convert or use other methods.

## Verify
Migration dashboard shows *Migration complete*; VM boots on the destination with the expected network; remove the network extension only after all VMs on that segment have moved and the gateway is cut over.
