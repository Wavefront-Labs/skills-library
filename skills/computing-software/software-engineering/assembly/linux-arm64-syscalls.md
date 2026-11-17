---
id: computing-software.software-engineering.assembly.linux-arm64-syscalls
name: linux-arm64-syscalls
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, linux-arm64-syscalls, asm-syscalls]
level: practitioner
status: docs-checked
description: "Linux arm64 raw system calls: number in X8, arguments X0-X5, SVC #0, the generic syscall table numbers, and no legacy open/fork."
sources:
  - https://man7.org/linux/man-pages/man2/syscall.2.html
  - https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/uapi/asm-generic/unistd.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Linux arm64 syscall ABI
**Goal:** call the Linux kernel from AArch64 assembly.

- Per the syscall(2) table: instruction `svc #0`, number in `w8`/`x8`, arguments in `x0`-`x5`, return value in `x0`.
- arm64 uses the generic syscall table (`include/uapi/asm-generic/unistd.h`), so numbers differ from x86-64: read 63, write 64, openat 56, close 57, exit 93, exit_group 94, getpid 172, mmap 222, munmap 215, clock_gettime 113, clone 220, pipe2 59.
- The generic table has `openat` and `pipe2` but defines no plain `open`, `fork` or `pipe` numbers (it has `clone`); use `openat` (`AT_FDCWD` for the current directory), `clone`, `pipe2`.
```asm
    .globl _start
    .text
_start:
    mov  x0, #1               // fd = stdout
    adr  x1, msg
    mov  x2, #3               // length
    mov  x8, #64              // write
    svc  #0
    mov  x0, #0
    mov  x8, #94              // exit_group
    svc  #0
msg: .ascii "hi\n"
```
- Build natively or cross with an AArch64 assembler and linker (for example `aarch64-linux-gnu-as hi.s -o hi.o && aarch64-linux-gnu-ld hi.o -o hi`) and run under an emulator on a non-Arm host.

## Gotchas
- Copying x86-64 syscall numbers to arm64 gives wrong calls.
- Data placed after code in `.text` works for a demo but should live in `.rodata`.
- Which registers the kernel preserves across `svc` is defined in the kernel's arm64 syscall ABI note, which was not read here; do not assume more than the table above states.

## Self-check
Print a string and exit with status 5 via raw syscalls, then check `echo $?`.

## Checked
2026-11-02. Checked against syscall(2) (arm64 row: `svc #0`, `w8`, `x0`-`x5`, return `x0`) and the kernel's asm-generic `unistd.h` (every number listed above). Removed: the `AT_FDCWD` value of -100, the specific qemu command, and the claim that the kernel preserves all registers except `x0`.

Method: documentation only; no commands were run.
