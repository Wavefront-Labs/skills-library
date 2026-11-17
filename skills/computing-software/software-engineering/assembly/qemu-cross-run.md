---
id: computing-software.software-engineering.assembly.qemu-cross-run
name: qemu-cross-run
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, qemu-cross-run, asm-containers-ci]
level: practitioner
status: draft
description: "Run and debug foreign-architecture assembly with qemu-user and cross toolchains, including the GDB stub and qemu-system for bare-metal images."
sources:
  - https://sourceware.org/gdb/documentation/
  - https://llvm.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# qemu-user and cross-toolchains
**Goal:** test AArch64 (or x86-64) assembly on any host.

```sh
# Debian/Ubuntu packages (names may vary by release)
sudo apt install qemu-user gcc-aarch64-linux-gnu binutils-aarch64-linux-gnu gdb-multiarch

aarch64-linux-gnu-as hi.s -o hi.o
aarch64-linux-gnu-ld hi.o -o hi
qemu-aarch64 ./hi                               # run a static binary
qemu-aarch64 -L /usr/aarch64-linux-gnu ./dyn    # dynamic: supply the target sysroot
qemu-aarch64 -g 1234 ./hi &                     # open a GDB stub, wait for the debugger
gdb-multiarch -ex 'target remote :1234' ./hi

qemu-system-aarch64 -M virt -cpu cortex-a57 -nographic -kernel kernel.elf     # bare metal
```
- `qemu-user` translates syscalls, so Linux user-mode programs run unmodified; `binfmt_misc` registration (the `qemu-user-static` package) lets you execute foreign binaries directly.
- Use `-cpu max` to expose the most CPU features for testing extensions such as SVE or LSE; select a specific model to test baseline behaviour.
- Emulation is functionally accurate but not cycle accurate, and its memory-ordering behaviour is stricter or different from hardware: never use it for performance or weak-memory conclusions.

## Gotchas
- Dynamic binaries need the matching libc under `-L`.
- `gdb` must be the multi-arch build, or `target remote` rejects the architecture.

## Self-check
Run the arm64 hello program under qemu-user and single-step it with gdb-multiarch.
