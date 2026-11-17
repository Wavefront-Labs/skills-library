---
id: computing-software.digital-forensics-incident-response.volatility.suspicious-threads-and-start-addresses
name: suspicious-threads-and-start-addresses
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [suspicious-threads, code-injection, process-injection, volatility3, dfir]
level: advanced
status: draft
description: "Hunt injected code via threads: windows.threads / suspicious_threads, start addresses outside modules, thread call stacks and APC/early-bird injection signs."
sources: ["https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.html", "https://attack.mitre.org/techniques/T1055/", "https://github.com/volatilityfoundation/volatility3"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Suspicious threads and start addresses

**Goal:** injected code must run on a thread. Threads whose start address is not inside a mapped
image (DLL/EXE) are one of the strongest injection indicators and survive header wiping.

## Volatility 3
```bash
vol -f mem.raw windows.threads | grep -w 4120             # windows.threads has no --pid option (checked in 2.28.2); filter the output
vol -f mem.raw windows.malware.suspicious_threads                 # threads whose start address is in non-image/unknown memory (newer releases)
vol -f mem.raw windows.vadinfo --address <start_addr> --pid 4120   # what backs the start address
```
- For each thread: is `Win32StartAddress` inside a VAD of type Image with a file name? If it points
  into private memory or a VAD without a file object -> suspicious.
- Thread **create time** clusters show when injection happened; correlate with process start and network events.

## Patterns
| Pattern | Indicator |
|---|---|
| CreateRemoteThread injection | New thread in target process starting in private RWX memory |
| Thread start spoofing | Start address = `ntdll!RtlUserThreadStart` or `kernel32!BaseThreadInitThunk` variant pointing to a stomped module region |
| APC / Early Bird injection | Threads in suspended-then-resumed processes; queued APCs (not directly listed, infer from shellcode location and thread state) |
| Thread hijacking | Existing thread's context changed: start address legitimate, but current instruction pointer in private memory (needs stack/context analysis) |

## Complement
- `windows.malware.malfind` on the VAD containing the start address; dump with `windows.memmap --dump --pid`.
- Live: Get-InjectedThread (PowerShell), PE-sieve thread scanning.

## Gotchas
- .NET and browsers create threads in JIT memory legitimately.
- Some plugins depend on symbol accuracy; mismatched ISF produces garbage addresses - confirm with windows.info.

## Verify
Each suspicious thread is mapped to its backing memory, dumped and classified.
