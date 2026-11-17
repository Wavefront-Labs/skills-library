---
id: computing-software.digital-forensics-incident-response.volatility.virtualbox-core-dumps-and-saved-states
name: virtualbox-core-dumps-and-saved-states
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [virtualbox-memory, vboxmanage, dumpvmcore, vm-memory, volatility3, dfir]
level: practitioner
status: docs-checked
description: "Capture and analyse VirtualBox guest memory: VBoxManage debugvm dumpvmcore ELF cores, saved-state .sav files and their limits, and opening cores in Volatility 3 and MemProcFS."
sources: ["https://www.virtualbox.org/manual/ch08.html", "https://github.com/volatilityfoundation/volatility/wiki/Virtual-Box-Core-Dump", "https://github.com/volatilityfoundation/volatility3", "https://github.com/ufrisk/MemProcFS"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VirtualBox core dumps and saved states

VirtualBox guests appear in malware labs, developer laptops and insider cases (a VM used to hide activity). Hypervisor-level capture gives memory without running a tool in the guest.

## Capture a core dump (preferred)
```bash
VBoxManage list runningvms
VBoxManage debugvm "<vm name or uuid>" dumpvmcore --filename=/evidence/guest.elf
```
The command creates a system dump in the standard ELF core format with custom sections; it corresponds to the `writecore` debugger command. Per the Volatility 2 wiki it is an ELF64 whose PT_LOAD segments hold guest physical memory. Hash the file and record VM name, UUID, VirtualBox version and host time.
The Volatility 2 wiki also describes starting a VM with `--dbg` and using the `.pgmphystofile` command to write a raw dd-style physical memory dump; only the ELF64 route needs special handling.

## Analyse
- Volatility 3 ships an ELF64 layer (`layers/elf.py`) that maps PT_LOAD program headers; try `vol -f guest.elf windows.info` (or `banners.Banners` for Linux guests) to confirm it works on your core before other plugins. If it does not, extract the PT_LOAD segments (p_paddr = physical start, p_offset = file offset, p_memsz = size) to a raw image.
- Volatility 2 had a dedicated VirtualBox address space and a `vboxinfo` plugin that shows the VBCORE header and memory ranges (RAM below 3.5 GB sits in the first run; the remainder starts at 0x100000000, with VGA and MMIO ranges between); its `imagecopy` converts a core to raw. That wiki is archived.
- MemProcFS `-device` accepts ELF full core dumps (VirtualBox).

## Saved states (.sav)
`VBoxManage controlvm <vm> savestate` saves the VM state to disk and stops the VM; restarting resumes exactly where it was. The Volatility 2 wiki notes VirtualBox does not write a full RAM dump when you suspend or pause a VM. The saved-state file format and location were not confirmed in the sources read and no tool support for parsing it was found:
- To obtain an ELF core, resume the VM on an isolated, network-disconnected host and `dumpvmcore`. This changes the VM, so document it and work on a copy of the VM folder.
- Preserve the saved-state file as evidence regardless.

## Guest disk alongside
Collect the VM's disk images, its `.vbox` configuration and the snapshot folder (`Snapshots/` in the machine folder by default). Log files are not covered by the sources read; preserve any `Logs/` folder anyway.

## Gotchas
- Running VirtualBox commands on a suspect's host changes host state; record actions and consider host imaging first (practitioner guidance).

## Verify
The core dump's hash is recorded, Volatility identifies the guest OS and lists processes, and the VM configuration is preserved with it.

## Checked

- Confirmed: dumpvmcore --filename produces ELF core with custom sections; --dbg and .pgmphystofile raw route; vboxinfo and imagecopy in Volatility 2; Vol3 ELF64 layer; savestate semantics.

Method: docs-checked 2026-11-09 against VirtualBox manual ch08 (debugvm dumpvmcore, controlvm savestate, snapshot folder), Volatility 2 wiki Virtual-Box-Core-Dump, volatility3 layers/elf.py and MemProcFS README. ch12 and the Volatility 3 readthedocs index were not read and were dropped; SSM format, .sav location and VBox.log claims were removed as unconfirmed.
