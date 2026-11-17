---
id: computing-software.digital-forensics-incident-response.evidence-handling.acquiring-virtual-machine-disks-and-snapshots
name: acquiring-virtual-machine-disks-and-snapshots
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [vm-acquisition, vmdk, vhdx, hypervisor-forensics, snapshots, forensic-acquisition, dfir]
level: practitioner
status: draft
description: "Acquire virtual machine evidence from VMware, Hyper-V and cloud hypervisors: snapshots with memory, exporting VMDK/VHDX, delta disks, and hashing."
sources: ["https://docs.vmware.com/en/VMware-vSphere/index.html", "https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/choose-between-standard-or-production-checkpoints-in-hyper-v"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Acquiring virtual machine disks and snapshots

**Goal:** capture VM disk and memory from outside the guest, with minimal impact and a
consistent point in time.

## VMware vSphere / ESXi
1. Take a snapshot **with memory** (`Snapshot the virtual machine's memory` ticked; do
   not quiesce, which runs guest tools scripts). Produces `.vmsn` / `.vmem` (memory) and a
   new delta disk; the base `-flat.vmdk` stops changing.
2. Copy the base `.vmdk` descriptor + `-flat.vmdk`, prior deltas (`-00000N-delta.vmdk` or
   `-sesparse.vmdk`), `.vmsn`, `.vmem`, `.vmx`, and `vmware.log` via datastore browser,
   `scp` from ESXi, or `vmkfstools -i src.vmdk dst.vmdk -d thin` for consolidated copy.
3. Hash all copied files.
Alternatively suspend the VM (`.vmss` + `.vmem`).

## Hyper-V
`Checkpoint-VM -Name VM1 -SnapshotName IR-014` (standard checkpoint saves memory state in
`.vmrs`); export: `Export-VM -Name VM1 -Path \export`. Differencing `.avhdx` chains must
be kept with parent `.vhdx`.

## Analysis
- Convert/mount: `qemu-img convert -O raw disk.vmdk disk.raw`, or mount `.vmdk`/`.vhdx`
  directly with Arsenal Image Mounter, `libvmdk`/`libvhdi` (`vmdkmount`, `vhdimount`).
- Memory: Volatility 3 reads `.vmem` (with `.vmss`/`.vmsn` for metadata) directly.

## Cloud
See cloud snapshot procedures (EBS/managed disk/persistent disk snapshots) for IaaS.

## Gotchas
- Snapshots on a busy VM grow fast; remove the IR snapshot after copying (consolidation
  merges changes back).
- Thin-provisioned disks copy at allocated size; the logical size may be larger.
- ESXi hosts themselves can be the compromised system (ransomware on ESXi); collect host
  logs (`/var/log/hostd.log`, `auth.log`, `shell.log`) too.

## Verify
The disk chain opens in your tool without missing-parent errors and hashes are recorded
for every file in the chain.
