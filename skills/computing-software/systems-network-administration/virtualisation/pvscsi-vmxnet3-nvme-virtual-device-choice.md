---
id: computing-software.systems-network-administration.virtualisation.pvscsi-vmxnet3-nvme-virtual-device-choice
name: pvscsi-vmxnet3-nvme-virtual-device-choice
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pvscsi-vmxnet3-choice, pvscsi, vmxnet3, nvme-controller, vsphere-vm-administration, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Pick VM virtual hardware: PVSCSI vs LSI SAS vs NVMe controller, VMXNET3 vs E1000E, multiple controllers for I/O, queue depth tuning and safe in-place conversion."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-virtual-machine-administration-guide-8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual device choice: storage controllers and NICs

## Storage controller
| Controller | Use |
|---|---|
| **PVSCSI** | Default for servers with VMware Tools; lowest CPU per I/O, highest queue depth |
| LSI Logic SAS | OS without PVSCSI driver at install (older Windows), WSFC legacy |
| **NVMe** controller | All-flash/NVMe backends; low CPU; check guest OS support |
| SATA | CD-ROM, odd guests |

I/O-heavy VMs (SQL, Oracle): spread data, log and tempdb across multiple controllers.

### PVSCSI queue depth
Queue-depth tuning for PVSCSI (Windows registry DriverParameter, Linux module parameters)
only helps with backend storage that can absorb the extra I/O; see current VMware
guidance before changing it.

### Converting boot disk LSI → PVSCSI (Windows)
1. Add a **second** PVSCSI controller with a small temp disk; boot so Windows loads the
   driver. 2. Shut down, change the boot controller type to PVSCSI, remove temp disk.
Skipping step 1 gives INACCESSIBLE_BOOT_DEVICE.

## Network adapter
| Adapter | Use |
|---|---|
| **VMXNET3** | Default paravirtual NIC; needs the VMware Tools driver |
| E1000E | Install-time fallback only; higher CPU |
| SR-IOV / UPT passthrough | latency-sensitive NFV; loses vMotion (UPT on DPU excepted) |

VMXNET3 tuning for high pps: enable RSS in the guest and raise receive ring sizes; see
current VMware guidance for the guest-specific settings.

## Gotchas
- Changing NIC type creates a new NIC in the guest: static IP config stays on the
  old ghost adapter (Windows); reapply IP.
- NVMe controller does not support hot-add of the controller itself on older HW versions.

## Verify
Audit SCSI controller and network adapter types across VMs (PowerCLI or govc); only
justified exceptions remain.

## Checked
2026-10-31: The virtual-device choice topic confirmed to exist in the vSphere Virtual Machine Administration guide (TOC); PVSCSI/VMXNET3 named as the paravirtual device types in the guide structure. Removed all unconfirmed figures and commands: queue-depth defaults (64/254), the Windows registry and Linux module parameter examples, the HW 13+ NVMe gate, the 4-controller limit, guest OS lists, NIC speed support, the ethtool example and the PowerCLI audit commands.
Method: documentation only; no commands were run.
