---
id: computing-software.systems-network-administration.virtualisation.vm-lifecycle-snapshots-and-migration
name: vm-lifecycle-snapshots-and-migration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [virtualisation, virtualization, vmware, vsphere, esxi, vcenter, proxmox, proxmox-ve, kvm, qemu, hyper-v, scvmm, vm-template, cloud-init, sysprep, snapshot, checkpoint, vmotion, live-migration, evc, cpu-compatibility, overcommit, cpu-ready, ballooning, vmware-tools, open-vm-tools, qemu-guest-agent, integration-services, hypervisor]
level: practitioner
status: docs-checked
description: "VM lifecycle on vSphere/ESXi, Proxmox VE and Hyper-V: templates, snapshot gotchas (not backups), live migration prerequisites, EVC/CPU compatibility, overcommit."
sources:
  - https://docs.vmware.com/en/VMware-vSphere/index.html
  - https://pve.proxmox.com/pve-docs/
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/hyper-v-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM lifecycle, snapshots and migration — build from templates, snapshot briefly, migrate cleanly

**Goal:** provision consistent VMs fast, use snapshots without wrecking storage, and keep
live migration working across a cluster on any of the three common platforms.

## 1. Build from templates, not by cloning pets
| Step | vSphere | Proxmox VE | Hyper-V |
|---|---|---|---|
| Golden image | VM → Convert to Template / Content Library | `qm template <VMID>` | Sysprepped VHDX in a library share (or SCVMM template) |
| Customise on deploy | Guest OS customisation spec | cloud-init drive (`qm set <VMID> --ide2 <STORAGE>:cloudinit`) | Unattend.xml / cloud-init (Linux) |
| Fast copy | Instant Clone | Linked clone (`qm clone <VMID> <NEWID>`; omit `--full`) | Differencing disk |

- Windows templates must be generalised (`sysprep /generalize /oobe /shutdown`) or
  domain joins and WSUS see duplicate SIDs/IDs. Linux templates: clear
  `/etc/machine-id` (truncate it, do not delete), SSH host keys and DHCP leases.
- Linked clones depend on the template disk forever; use full clones for production.
- Patch templates monthly, or every new VM starts a month behind.

## 2. Snapshots are not backups
A snapshot is a **delta file chained to the base disk on the same datastore**. Lose the
datastore, or corrupt the chain, and every "backup" goes with it.
- Every write lands in the delta, which grows until deleted; a busy DB server can fill a
  datastore in hours and pause **every** VM on it.
- Long chains degrade I/O. Keep snapshots short-lived and chains short; verify current
  limits in the VMware documentation before setting policy.
- Deleting (consolidating) an old, large snapshot is I/O-heavy and can stun the VM;
  do it out of hours.
- **Memory snapshots** and **quiesced** snapshots are different things: memory state
  allows revert-to-running; quiescing (via guest tools/VSS) gives a file-system-consistent
  point. Neither makes a database transactionally safe on its own.
- Hyper-V: use **Production checkpoints** (VSS/fsfreeze inside the guest) for servers;
  Standard checkpoints include memory and can break apps that track time or replication.
- Avoid reverting domain controllers or replicated DBs via snapshot; prefer the app's own restore.

Policy: snapshot before a change, delete within your policy window after success. Alert
on snapshots older than the policy allows (RVTools, PowerCLI, `qm listsnapshot`).
Proper backups use the platform's backup APIs (VADP/CBT, Proxmox Backup Server, Hyper-V
RCT) to copy to separate storage.

## 3. Live migration prerequisites
- **Network:** a dedicated migration network/VMkernel (vMotion), same VM port
  groups/bridges/virtual switch names on both hosts (a missing network name blocks the move).
- **Storage:** shared storage, or storage migration together with compute (vSphere
  Storage vMotion; Proxmox `qm migrate <VMID> <NODE> --online --with-local-disks`;
  Hyper-V "shared nothing" migration). Expect it to take much longer with local disks.
- **CPU compatibility:** guests see CPU features at power-on and cannot lose them live.
  - vSphere: enable **EVC** on the cluster at the oldest CPU generation present. Easiest
    to set before VMs run; raising it later needs VM power cycles. No live migration
    between Intel and AMD.
  - Proxmox: CPU type `host` is fastest but pins the VM to identical hardware. Use a
    generic model for mixed clusters.
  - Hyper-V: "Processor compatibility" in VM settings (VM must be off to change).
- **Same or compatible hypervisor version** and time synced (NTP) on all hosts.

## 4. Sizing and overcommit
- **CPU:** start with modest CPU overcommit for general servers and near 1:1 for
  latency-sensitive or busy DB hosts. Measure, don't assume: sustained vSphere CPU Ready
  indicates contention. Right-size oversized VMs down.
- **Memory:** avoid overcommitting production memory. Ballooning, compression and
  host swapping all mean a slow guest.
- **Storage:** thin provisioning is overcommit too; alert well before the datastore is
  full.
- Keep N+1 capacity so one host can fail or enter maintenance mode and the rest absorb its VMs.

## 5. Guest tools
Install and keep current: VMware Tools / **open-vm-tools** (Linux), **qemu-guest-agent**
(enable the agent option in Proxmox too), Hyper-V Integration Services (built into
supported Windows and Linux kernels). Without them: no clean shutdown, no quiesced
snapshots, wrong IP reporting, and poorer drivers. Use paravirtual devices (VMXNET3,
PVSCSI, VirtIO); Windows on Proxmox needs the VirtIO drivers.

## Verify
- [ ] New VMs come from a generalised, patched template with unique machine IDs.
- [ ] No snapshot older than your policy allows exists; an alert catches the next one.
- [ ] A test VM live-migrates both ways between every host pair in the cluster.
- [ ] EVC / CPU compatibility set to the oldest CPU generation present.
- [ ] Cluster survives one host in maintenance mode without memory overcommit.
- [ ] Guest tools report running and current on every VM.

## Checked
2026-10-31: `qm template`, `qm set`, `qm clone` (with `--full`), `qm migrate` (with `--online` and `--with-local-disks`), `qm listsnapshot` and the cloud-init drive options confirmed in the Proxmox qm.1 man page; shared-nothing live migration and Hyper-V snapshot behaviour confirmed on the Microsoft Learn Hyper-V overview page. Removed unconfirmed figures: the 72 h/32-snapshot limits, vCPU ratios, 10 GbE, 5%/1000 ms CPU-ready threshold, 80% datastore alert and the PVE 8 default CPU model.
Method: documentation only; no commands were run.
