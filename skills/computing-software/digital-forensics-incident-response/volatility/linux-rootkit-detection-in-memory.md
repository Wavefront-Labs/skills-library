---
id: computing-software.digital-forensics-incident-response.volatility.linux-rootkit-detection-in-memory
name: linux-rootkit-detection-in-memory
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [linux-rootkit-detection, volatility3, check_syscall, check_modules, hidden-modules, lkm-rootkit, linux-memory-forensics, dfir]
level: advanced
status: docs-checked
description: "Detect Linux kernel rootkits in a memory image with Volatility 3 check_syscall, check_modules, hidden-module, IDT and tty checks, and confirm hooks."
sources: ["https://volatility3.readthedocs.io/en/latest/volatility3.plugins.linux.html", "https://github.com/volatilityfoundation/dwarf2json", "https://github.com/volatilityfoundation/volatility3"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Linux rootkit detection in memory (check_syscall and friends)

**Goal:** prove or rule out a loadable-kernel-module (LKM) or eBPF rootkit on a Linux host
using memory, because on-host tools run through the hooks the rootkit installed.

## Prerequisites
- A memory image in a format Volatility 3 reads (it has LiME and AVML layers).
- A matching symbol table: build from the exact kernel's debug symbols:
  `dwarf2json linux --elf vmlinux-<ver>-dbg --system-map System.map-<ver> > <ver>.json`,
  place it under `volatility3/symbols/linux/`. Without matching symbols Volatility cannot
  analyse the image.

## Checks
```bash
vol -f mem.lime linux.malware.check_syscall     # system call table hooks
vol -f mem.lime linux.malware.check_modules     # compares the module list to sysfs info, if available
vol -f mem.lime linux.malware.hidden_modules    # carves memory for hidden kernel modules
vol -f mem.lime linux.malware.modxview          # centralises lsmod, check_modules and hidden_modules results
vol -f mem.lime linux.lsmod             # loaded modules list
vol -f mem.lime linux.malware.check_idt         # whether the IDT has been altered
vol -f mem.lime linux.malware.check_afinfo      # network protocol operation pointers (seq_ops/seq_show)
vol -f mem.lime linux.malware.tty_check         # tty devices for hooks (line-discipline receive_buf)
vol -f mem.lime linux.malware.keyboard_notifiers  # keyboard notifier call chain
vol -f mem.lime linux.malware.check_creds       # processes sharing credential structures
vol -f mem.lime linux.malware.netfilter         # Netfilter hooks
vol -f mem.lime linux.malware.malfind           # process memory ranges that may contain injected code
vol -f mem.lime linux.pslist ; vol -f mem.lime linux.pidhashtable   # compare: process hidden from task list
```

## Interpretation
- A `check_syscall` row whose handler does not resolve to the kernel image (for example it
  resolves into a module) is a hook.
- Rootkits that unlink themselves from the module list are what `check_modules` and
  `hidden_modules` are for. To get the module back as a file, use `linux.module_extract`
  (it recreates an ELF from a kernel address given with `--base`) and analyse it statically.
- Rootkits that hook via ftrace instead of the syscall table will not show in
  `check_syscall`; review `linux.tracing.ftrace` and `linux.kthreads` in recent builds.
- eBPF-based rootkits: check `linux.ebpf` (enumerates eBPF programs) in recent builds for
  programs you cannot account for.

## Gotchas
- Some security products (EDR agents, livepatch) legitimately hook; identify the owning
  module before calling it malicious.
- Cross-check with disk: module `.ko` on disk, `/etc/modules-load.d/`, initramfs.

## Self-check
Each hook is attributed to a named module, the module is dumped/hashed, and the persistence
path that reloads it at boot is identified.

## Checked

- Confirmed: every listed plugin exists with the stated purpose; dwarf2json linux --elf/--system-map flags.

Method: docs-checked 2026-11-09 against volatility3 develop source plugins/linux/malware/*.py, linux/{lsmod,pidhashtable,ebpf,kthreads,module_extract,tracing/ftrace}.py, layers (lime, avml) and the dwarf2json README. Removed unconfirmed LiME command, rootkit family names, syscall target list, debugfs path and bpftool command.
