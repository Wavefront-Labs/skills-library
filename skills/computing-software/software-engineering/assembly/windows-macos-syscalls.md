---
id: computing-software.software-engineering.assembly.windows-macos-syscalls
name: windows-macos-syscalls
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, windows-macos-syscalls, asm-syscalls]
level: sme
status: draft
description: "Direct syscalls on Windows (ntdll stubs, build-specific numbers) and macOS (class-prefixed numbers, X16 on arm64): why to prefer system libraries."
sources:
  - https://learn.microsoft.com/en-us/cpp/build/x64-software-conventions
  - https://man7.org/linux/man-pages/man2/syscall.2.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Windows ntdll and macOS syscalls
**Goal:** know what is stable and what is not outside Linux.

- Windows: user code calls `kernel32`/`ntdll` APIs. The native NT stubs in `ntdll.dll` load a system service number into `eax`, move `rcx` to `r10` and execute `syscall`:
```nasm
NtSomething:
    mov  r10, rcx
    mov  eax, <service-number>     ; changes between Windows builds
    syscall
    ret
```
  The numbers change from build to build and are not a supported interface; call the exported function instead of embedding a number.
- macOS x86-64: syscall class in the high bits of `rax` (BSD class is `0x2000000`): exit is `0x2000001`, write is `0x2000004`; arguments in `rdi, rsi, rdx, r10, r8, r9`; errors set the carry flag.
```nasm
    mov  eax, 0x2000001           ; exit
    xor  edi, edi
    syscall
```
- macOS arm64: number in `x16`, `svc #0x80`. Apple documents libSystem, not raw syscalls, as the stable interface.
- Prefer the platform library (kernel32, libSystem) in anything shipping.

## Gotchas
- Hard-coded syscall numbers break on OS updates (Windows) and violate platform guidance (macOS).
- Endpoint security software flags direct syscalls on Windows.

## Self-check
Write a macOS x86-64 program that exits with status 3 using the class-prefixed number.
