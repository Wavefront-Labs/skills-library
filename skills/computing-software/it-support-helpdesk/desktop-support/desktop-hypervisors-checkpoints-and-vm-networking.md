---
id: computing-software.it-support-helpdesk.desktop-support.desktop-hypervisors-checkpoints-and-vm-networking
name: desktop-hypervisors-checkpoints-and-vm-networking
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, desktop-hypervisor, vm-checkpoints, vm-networking, virtualbox, vmware-workstation, hyper-v]
level: practitioner
status: draft
description: "Support desktop hypervisors (Hyper-V, VirtualBox, VMware Workstation): coexistence with VBS, checkpoints and snapshots for testing, and NAT, bridged and internal VM networking."
sources:
  - "https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/user-guide/checkpoints"
  - "https://www.virtualbox.org/manual/topics/networkingdetails.html"
  - "https://docs.vmware.com/en/VMware-Workstation-Pro/17/com.vmware.ws.using.doc/GUID-0CE1AE01-7E79-41BB-9EA8-4F839BE40E1A.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# desktop-hypervisors-checkpoints-and-vm-networking

## Coexistence
- Hyper-V, WSL2, Windows Sandbox, VBS/Memory Integrity and Credential Guard all use the
  Windows hypervisor. VirtualBox (6.0+) and VMware Workstation (15.5.5+) run on top of it
  via the Windows Hypervisor Platform, slower than native but working.
- Old versions fail with "VT-x is not available" or performance is poor. Update the
  product rather than disabling VBS (a security control).
- BIOS: Intel VT-x/AMD-V and VT-d enabled.

## Checkpoints / snapshots for testing
- Hyper-V: **Standard** checkpoints save memory state; **Production** checkpoints use
  VSS inside the guest (application-consistent, no memory). For test VMs, standard is
  fine.
  `Checkpoint-VM -Name TestVM -SnapshotName "before-update"`;
  `Restore-VMCheckpoint -Name "before-update" -VMName TestVM -Confirm:$false`.
- VirtualBox: Machine > Take Snapshot; `VBoxManage snapshot TestVM take before-update`.
- VMware: VM > Snapshot > Take Snapshot.
- Workflow: clean baseline, checkpoint, test the update/app/script, revert, repeat.
- Snapshots are not backups; long chains slow disks and grow. Delete when done.
- Domain-joined VMs reverted far back break the computer account password (trust
  relationship errors); use non-domain test VMs or rejoin.

## VM networking modes
| Mode | VM gets | Reachable from LAN | Use |
|---|---|---|---|
| NAT | Private IP behind host | No (port forwarding only) | Internet access for tests |
| Bridged | Own IP on the LAN | Yes | VM acts like a real PC |
| Host-only / Internal | Private network with host (or VMs only) | No | Isolated malware/test labs |
| Hyper-V Default Switch | NAT with DHCP | No | Quick setup |
| Hyper-V External switch | Bridged to a physical NIC | Yes | Servers/labs |
- Bridged on Wi-Fi often fails with 802.1X or MAC limits; use NAT.
- Corporate networks may block unknown MACs (NAC); bridged VMs then get no IP.
- Hyper-V external switches take over the NIC; creating one briefly drops host network.

## Verify
The VM starts with the hypervisor coexisting with VBS, a checkpoint restores to the
expected state, and the VM has network access in the intended mode.
