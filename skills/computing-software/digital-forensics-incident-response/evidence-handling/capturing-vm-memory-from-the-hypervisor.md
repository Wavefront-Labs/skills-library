---
id: computing-software.digital-forensics-incident-response.evidence-handling.capturing-vm-memory-from-the-hypervisor
name: capturing-vm-memory-from-the-hypervisor
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [vm-memory-capture, memory-acquisition, vmem, hyper-v, vmware, dfir]
level: practitioner
status: draft
description: "Capture virtual machine memory from the hypervisor (VMware vmem/vmss/vmsn, Hyper-V vmrs, KVM virsh dump, cloud) without running tools in the guest."
sources: ["https://volatility3.readthedocs.io/en/latest/", "https://libvirt.org/manpages/virsh.html", "https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/choose-between-standard-or-production-checkpoints-in-hyper-v"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capturing VM memory from the hypervisor

**Goal:** a memory image of a guest taken from outside, so guest-level rootkits and
anti-forensics cannot interfere and no tool touches the guest.

## VMware (ESXi / Workstation)
- **Snapshot with memory** -> `<vm>-Snapshot<N>.vmsn` + `.vmem`; or **suspend** -> `.vmss`
  + `.vmem`. Copy the `.vmem` together with the `.vmss`/`.vmsn` (Volatility uses the latter
  for layout metadata on newer versions).
- Volatility 3 opens `.vmem` directly: `vol -f vm-Snapshot1.vmem windows.info`.
- ESXi CLI: `vim-cmd vmsvc/getallvms`, `vim-cmd vmsvc/snapshot.create <vmid> IR-014 "" 1 0`
  (includeMemory=1, quiesce=0).

## Hyper-V
- Standard checkpoint saves memory in `.vmrs` (and `.vmgs` for Gen2 guest state). Convert
  with Microsoft's `vm2dmp.exe` to a crash dump, or use MemProcFS / Volatility layers that
  support Hyper-V saved state. Alternatively `Save-VM` (saved state) and copy files.
- `Debug-VM -Name VM1 -InjectNonMaskableInterrupt` can trigger a guest crash dump if
  configured, but changes guest state; prefer checkpoints.

## KVM / QEMU
```bash
virsh dump --memory-only --format elf vm1 /evid/vm1.elf   # guest memory as ELF core
virsh qemu-monitor-command vm1 --hmp 'dump-guest-memory -z /evid/vm1.dmp'
```
Volatility 3 reads ELF core dumps.

## Cloud
Few providers expose guest memory externally; use in-guest tools (AVML/WinPmem via SSM/Run
Command) or provider-specific options (e.g. Azure VM memory via in-guest only). Hibernate-
to-disk on AWS EC2 writes memory to the EBS root volume which can then be snapshotted.

## Verify
`vol -f <image> windows.info` (or `banners.Banners` for Linux) identifies the kernel and the
time of capture matches your notes; hash the memory files at copy.
