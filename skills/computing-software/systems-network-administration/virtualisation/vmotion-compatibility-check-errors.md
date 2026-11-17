---
id: computing-software.systems-network-administration.virtualisation.vmotion-compatibility-check-errors
name: vmotion-compatibility-check-errors
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [migration-compatibility-check, vmotion, vmotion-failure, evc, vsphere-troubleshooting, vmware, vsphere]
level: practitioner
status: draft
description: "Decode vMotion compatibility check errors and warnings (CPU features, devices, networks, datastores, vmk) and fix each class before migrating."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-and-host-management-8-0.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vMotion compatibility check errors

The migrate wizard's **Compatibility** panel runs checks before any data moves. Errors
block; warnings allow. Same checks run for DRS, so a VM that fails here is also stuck for
maintenance mode.

## Common errors and fixes
| Message (abridged) | Cause | Fix |
|---|---|---|
| "The target host does not support the virtual machine's current hardware requirements" / CPU feature mismatch (e.g. `cpuid.AVX512`) | Different CPU generations, no EVC | Enable cluster EVC at the oldest baseline, or per-VM EVC; VM must power-cycle to drop features |
| "Currently connected device 'CD/DVD drive 1' uses backing '...iso' which is not accessible" | ISO on local datastore or client device | Disconnect CD or move ISO to shared datastore |
| "Network interface 'Network adapter 1' uses network 'X', which is not accessible" | Port group missing on target | Create matching port group or use vDS |
| "Unable to access file ... on datastore" | Datastore not mounted on target | Mount datastore or use storage vMotion simultaneously |
| "vMotion is not enabled on the source/destination host" | No vmk tagged vMotion | Tag a vmk (or vMotion TCP/IP stack) |
| "Virtual machine is configured to use a device that prevents the operation: PCI passthrough / USB" | DirectPath, USB host device | Remove or use Assignable Hardware/vGPU with supported vMotion |
| "The virtual machine has a SCSI controller in bus sharing mode" | WSFC shared disk | Not movable live (except supported 7.0+ WSFC configs) |
| "Insufficient resources" / reservation | Target can't satisfy CPU/mem reservation | Lower reservation or pick another host |
| "Hardware version not supported" | Target ESXi older than VM HW version | Move to newer host or keep cluster homogeneous |

## Warnings worth reading
- "Network ... has no physical uplinks" (internal-only vSwitch): migration succeeds but VM
  loses connectivity.
- "Fault Tolerance..." / "vSphere HA..." informational.

## Diagnose further
```sh
grep -i vmotion /var/run/log/hostd.log | tail      # on source and target
grep -i "Migrate" /var/log/vmware/vpxd/vpxd.log     # on vCenter
```
Test vmk path: `vmkping -I vmk1 -S vmotion <dest-vmotion-ip>`.

## Verify
Re-run Migrate → Compatibility shows "Compatibility checks succeeded"; put the host into
maintenance mode and confirm DRS evacuates every VM.
