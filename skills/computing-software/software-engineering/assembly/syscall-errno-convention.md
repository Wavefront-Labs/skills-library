---
id: computing-software.software-engineering.assembly.syscall-errno-convention
name: syscall-errno-convention
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, syscall-errno-convention, asm-syscalls]
level: practitioner
status: draft
description: "Error reporting for raw syscalls: Linux returns negative errno in the result register, BSD-style kernels set the carry flag; converting to the libc convention."
sources:
  - https://man7.org/linux/man-pages/man2/syscall.2.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Return values and -errno
**Goal:** detect and decode syscall failures without libc.

- Linux: the kernel returns `-errno` in the result register. Any value in `-4095 .. -1` (as unsigned: at or above `0xFFFFFFFFFFFFF001`) is an error; other values are successful results (such as large addresses from `mmap`).
```nasm
    syscall
    cmp  rax, -4095
    jae  .error               ; unsigned compare catches -4095..-1
    ret                       ; success: rax = result
.error:
    neg  rax                  ; rax = errno (for example 2 = ENOENT)
    ret
```
- libc wrappers convert this to `-1` and set `errno`; a raw wrapper must do the same if C code depends on it.
- On arm64 the same range applies: test `x0` with `cmn x0, #4095` and `b.hi`.
```asm
    svc  #0
    cmn  x0, #4095            // x0 + 4095 carries when x0 >= -4095 unsigned
    b.hs error                // C set: x0 in -4095..-1
```
- BSD-derived kernels (FreeBSD, macOS) signal failure by setting the carry flag and returning a positive errno in the result register; check `jc` after `syscall` on those systems.
- Errno numbers are architecture independent on mainstream Linux ports for the common values (EPERM 1, ENOENT 2, EINTR 4, EAGAIN 11).

## Gotchas
- Testing `rax < 0` signed mishandles legitimate high addresses returned by `mmap` on systems with large address spaces.
- `EINTR` means retry for restartable calls such as `read`.

## Self-check
Call `open` on a missing file and print the decoded errno.
