---
id: computing-software.digital-forensics-incident-response.volatility.linux-code-injection-with-linux-malfind
name: linux-code-injection-with-linux-malfind
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [linux-malfind, volatility3, linux-memory-forensics, process-injection, memfd, dfir]
level: advanced
status: docs-checked
description: "Detect Linux process code injection with Volatility 3 linux.malware.malfind: RWX mappings, ptrace and memfd injection, JIT false positives, follow-up plugins."
sources: ["https://volatility3.readthedocs.io/en/latest/volatility3.plugins.linux.malware.malfind.html", "https://volatility3.readthedocs.io/en/latest/volatility3.plugins.linux.malfind.html", "https://volatility3.readthedocs.io/en/latest/volatility3.plugins.linux.proc.html", "https://volatility3.readthedocs.io/en/latest/volatility3.plugins.linux.html", "https://attack.mitre.org/techniques/T1055/008/", "https://man7.org/linux/man-pages/man2/memfd_create.2.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Linux code injection with linux.malware.malfind

`linux.malware.malfind` lists process memory ranges that potentially contain injected code; the older
`linux.malfind` module is marked deprecated in the plugin reference. Its flags include `RWX`. Injection
techniques on Linux include `ptrace` system calls (ATT&CK T1055.008, which injects code into the address
space of a separate live process) and anonymous in-memory files from `memfd_create`, which creates an
anonymous file.

## Run
```bash
vol -f mem.lime linux.malware.malfind
vol -f mem.lime linux.proc.Maps     # Maps lists all memory maps of all processes
```
Check `vol -h` and each plugin's `-h` for options such as PID filters and dumping; those are not in the
plugin reference pages.

## Interpreting
- Anonymous executable or writable-and-executable mappings in a process that should not generate code
  (a daemon, a cron job) are leads.
- Mappings backed by a `memfd` anonymous file with execute permission suggest a fileless payload.
- JIT engines (Java, V8, browsers, .NET and others) legitimately create RWX or anonymous executable
  memory, so judge hits in those processes by content, not flags alone.

## Follow-up
1. `linux.proc.Maps` exposes `vma_dump`, which extracts the data of a VMA; hash and analyse the dump
   with your normal tools.
2. Check the process environment with `linux.envars` and its process tree with `linux.pstree`; see also
   `linux.bash` and `linux.ptrace` for related evidence.
3. ATT&CK notes ptrace injection may not be possible against non-child or higher-privilege processes,
   and lists Yama (`/proc/sys/kernel/yama/ptrace_scope`), SELinux, grsecurity and AppArmor as
   mitigations.

## Gotchas
- Symbol tables must match the kernel; confirm the process list is sensible with `linux.pslist` first.

## Verify
Each reported injection has a dumped region with its hash and a description of the content, and the
injection method is supported by other evidence or marked as undetermined.

## Checked
2026-11-08. Read in full: linux.malware.malfind, linux.malfind and linux.proc plugin reference pages,
the linux plugin module list, MITRE T1055.008 and the memfd_create man page. Confirmed plugin names,
RWX flag, Maps and vma_dump, ptrace technique and mitigations. Removed unconfirmed claims: specific
options (--pid, --dump), output column list, ELF header byte pattern, deleted-mapping marker, the
LD_PRELOAD and /proc/pid/mem technique list, and hardened-kernel statements.
Method: documentation only; no commands were run.
