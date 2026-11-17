---
id: computing-software.software-engineering.assembly.aslr-pie-nx
name: aslr-pie-nx
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, aslr-pie-nx, asm-security]
level: practitioner
status: draft
description: "ASLR, position-independent executables and NX/W^X from the assembly author's view: what the loader randomises, how to check and what code must avoid."
sources:
  - https://refspecs.linuxfoundation.org/
  - https://learn.microsoft.com/en-us/cpp/build/x64-software-conventions
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# ASLR, PIE and NX
**Goal:** write assembly that runs under default OS hardening.

- ASLR randomises load addresses of the stack, heap, libraries and (for PIE) the executable itself. PIE binaries are ELF type `DYN`; a non-PIE executable is type `EXEC`.
- NX marks data pages non-executable; W^X policies forbid pages that are both writable and executable. Linux uses `PT_GNU_STACK` flags to decide whether the stack is executable.
```sh
readelf -h prog | grep Type           # DYN = PIE, EXEC = fixed address
readelf -lW prog | grep -E 'GNU_STACK|LOAD'
cat /proc/sys/kernel/randomize_va_space      # 2 = full randomisation
gcc -pie -fPIE -o prog main.c add.o
ld -z noexecstack -o prog obj.o
```
- Consequences for assembly: use RIP-relative or ADRP addressing, never absolute 32-bit address immediates; keep jump tables relative; add `.section .note.GNU-stack,"",@progbits` so the stack stays non-executable.
- Code generation at run time (JITs, trampolines) must map memory writable, then change it to executable with `mprotect`, rather than one RWX page.
- Debuggers disable ASLR by default (GDB: `set disable-randomization on`); remember that addresses differ outside the debugger.
- Windows equivalents: `/DYNAMICBASE` and `/NXCOMPAT` linker flags; images without base relocations cannot move.

## Gotchas
- Hard-coded addresses copied from a debugger session break on the next run.
- An executable stack is a finding in security scans; check it after linking.

## Self-check
Build with and without `-no-pie` and note the difference in printed addresses across runs.
