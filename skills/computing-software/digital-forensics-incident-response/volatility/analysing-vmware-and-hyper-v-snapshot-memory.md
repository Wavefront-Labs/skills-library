---
id: computing-software.digital-forensics-incident-response.volatility.analysing-vmware-and-hyper-v-snapshot-memory
name: analysing-vmware-and-hyper-v-snapshot-memory
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [vmware-vmem, vmss, vmsn, hyper-v-saved-state, vmss2core, volatility3, vm-memory, dfir]
level: practitioner
status: draft
description: "Analyse memory from VMware .vmem/.vmss/.vmsn and Hyper-V saved states: which files to collect, conversion with vmss2core, and Volatility 3 usage."
sources: ["https://volatility3.readthedocs.io/en/latest/", "https://github.com/ufrisk/MemProcFS"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Analysing VMware and Hyper-V snapshot memory

**Goal:** acquire memory of a virtual machine non-invasively by suspending or snapshotting it,
then analyse the resulting files.

## VMware (Workstation / ESXi)
- Suspend creates `<vm>.vmss` + `<vm>.vmem`; a snapshot with memory creates
  `<vm>-Snapshot<N>.vmsn` + `<vm>-Snapshot<N>.vmem`.
- The `.vmem` is the RAM; the `.vmss`/`.vmsn` holds the memory region layout. On VMs with
  more than about 3 GB of RAM, physical memory has a gap and the `.vmem` alone is
  misaligned: always copy the metadata file too.
- Volatility 3 detects VMware snapshots when the `.vmss`/`.vmsn` sits next to the `.vmem` with
  the same base name: `vol -f snap.vmem windows.info`.
- Conversion when a tool cannot read VMware formats:
  `vmss2core -W snap.vmsn snap.vmem` (Windows crash dump `memory.dmp`), `-M` for macOS,
  default output is an ELF core (`vmss.core`) for Linux/other.
- On ESXi, take the snapshot with "Snapshot the virtual machine's memory" ticked, then copy
  files from the datastore (`scp` from the ESXi shell or datastore browser download); hash on
  arrival.

## Hyper-V
- Saved state / checkpoints: `.vmrs` (Windows Server 2016+ / Win10) or older `.bin` + `.vsv`.
- Convert to a crash dump with Microsoft's `vmsavedstatedumpprovider`-based tooling
  (e.g. `VmSavedStateDumpProvider` sample / `vm2dmp` for older `.bin/.vsv`), then open in
  Volatility or WinDbg. Alternatively run a dump inside the guest or use
  `Debug-VM -Name <vm> -InjectNonMaskableInterrupt` with a configured crash dump to force a
  complete dump from the guest.

## Why this is preferred
Suspending a VM captures memory without running an acquisition tool in the guest, so no
footprint in the guest's memory and no chance for guest malware to interfere. Note the time of
the suspend in UTC and the host clock offset.

## Gotchas
- Suspending drops network sessions and may alert an attacker monitoring the host; decide
  with the incident lead.
- Cloud VMs (EC2/Azure/GCP) do not expose hypervisor memory; use in-guest tools (AVML,
  WinPmem, DumpIt) via SSM/Run Command.
- Encrypted VMs (VM encryption, Shielded VMs) produce encrypted memory files.

## Self-check
You copied both the memory and metadata files, hashed them, and `windows.info` (or the Linux
banner) reports a sane kernel base and build.
