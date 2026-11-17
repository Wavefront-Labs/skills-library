---
id: computing-software.software-engineering.assembly.svc-exception-levels
name: svc-exception-levels
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, svc-exception-levels, asm-arm64-system]
level: advanced
status: draft
description: "AArch64 exception levels EL0-EL3, SVC/HVC/SMC calls, ERET and exception vector basics for kernel and bare-metal work."
sources:
  - https://developer.arm.com/documentation/ddi0487/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# SVC and exception levels
**Goal:** understand privilege transitions on AArch64.

- Four levels: EL0 user, EL1 OS kernel, EL2 hypervisor, EL3 secure monitor. Higher number is more privileged.
- `svc #imm` raises a synchronous exception to EL1 (a system call); `hvc` goes to EL2; `smc` goes to EL3.
- On entry the CPU saves the return address in `ELR_ELn` and the processor state in `SPSR_ELn`; `eret` restores them and returns to the lower level.
- The syndrome register `ESR_ELn` encodes the cause; the vector table base is `VBAR_ELn`. The table has 16 entries of 128 bytes each, selected by source level and exception type (sync, IRQ, FIQ, SError).
```asm
// user-space system call on Linux/arm64
mov  x8, #93        // exit
mov  x0, #0
svc  #0
```
- The syscall numbering and register convention is OS specific (see linux-arm64-syscalls).

## Gotchas
- `svc` immediates are ignored by Linux; the syscall number is in `x8`.
- Do not use `svc` directly on macOS or Windows: syscalls there are only stable through system libraries (macOS uses `x16` and `svc #0x80`, unsupported API).

## Self-check
Write a program that exits with status 7 via `svc` and verify with `echo $?`.
