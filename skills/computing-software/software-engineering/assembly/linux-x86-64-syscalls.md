---
id: computing-software.software-engineering.assembly.linux-x86-64-syscalls
name: linux-x86-64-syscalls
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, linux-x86-64-syscalls, asm-syscalls]
level: practitioner
status: docs-checked
description: "Linux x86-64 raw system calls: number in RAX, arguments RDI RSI RDX R10 R8 R9, results in RAX/RDX, and common call numbers from the kernel table."
sources:
  - https://man7.org/linux/man-pages/man2/syscall.2.html
  - https://raw.githubusercontent.com/torvalds/linux/master/arch/x86/entry/syscalls/syscall_64.tbl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Linux x86-64 syscall ABI
**Goal:** invoke the kernel directly from assembly.

- Per syscall(2): the `syscall` instruction is the entry, the number goes in `rax`, arguments in `rdi, rsi, rdx, r10, r8, r9` (note `r10`, not `rcx`), and the return value comes back in `rax` (with `rdx` as a second return register).
- Common numbers (from `syscall_64.tbl`): read 0, write 1, open 2, close 3, mmap 9, munmap 11, brk 12, getpid 39, exit 60, exit_group 231, openat 257. Look up others in that table.
```nasm
; write(1, msg, len) then exit_group(0)
mov  eax, 1
mov  edi, 1
lea  rsi, [rel msg]
mov  edx, msglen
syscall
mov  eax, 231
xor  edi, edi
syscall
```
- The man page's table lists at most six argument registers for x86-64.

## Gotchas
- Using `rcx` for the fourth argument (as in the function ABI) is wrong for syscalls.
- syscall(2) warns that its register tables do not cover the whole calling convention: some architectures may clobber other registers not listed. Treat registers beyond the listed ones as not guaranteed, and consult the kernel's entry code for x86-64 clobber rules before relying on them.

## Self-check
Write a program that calls `getpid` (39) and exits with `pid & 0xff`; compare with `$$` in the shell.

## Checked
2026-11-08. Confirmed against the syscall(2) man page (x86-64 row: `syscall`, number in rax, return rax/rdx, argument registers rdi rsi rdx r10 r8 r9, the caveat about unlisted clobbers) and the Linux `syscall_64.tbl` (all eleven numbers). Removed: the `rcx`/`r11` clobber and "all other registers preserved" statements, the exit vs exit_group thread-semantics note, and the libc-features remark (none are on the cited pages).
Method: documentation only; no commands were run.
