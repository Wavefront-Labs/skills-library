---
id: computing-software.software-engineering.assembly.asm-build-systems
name: asm-build-systems
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, asm-build-systems, asm-project]
level: practitioner
status: gated
description: "Build assembly with Make and CMake: pattern rules for NASM and GAS, enable_language(ASM_NASM), preprocessor-enabled .S files and dependency handling."
sources:
  - https://www.nasm.us/doc/
  - https://sourceware.org/binutils/docs/as/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Makefile and CMake for asm
**Goal:** reproducible builds that rebuild when headers change.

```make
# Makefile
AS      = nasm
ASFLAGS = -f elf64 -g -F dwarf
%.o: %.asm common.inc
	$(AS) $(ASFLAGS) $< -o $@
```
(Make recipe lines begin with a tab.)
- Choose the NASM object format (`-f elf64`, `macho64`, `win64`) per platform. (gated: unconfirmed, source is paywalled or blocked)
- NASM can write dependency files with `-MD`; GCC uses `-MMD`. (gated: unconfirmed, source is paywalled or blocked)
- List include files such as `common.inc` as prerequisites so changes rebuild dependents.

## Gotchas
- Forgotten `.inc` dependencies cause stale objects.

## Self-check
Edit `common.inc`, run `make`, and verify only dependent objects rebuild.
## Checked
2026-11-02. The NASM documentation index was read but the option pages (output formats, `-M` options) were not; the NASM flags above are gated. Removed: all CMake and Meson claims and the GAS `.S` rule (GAS manual not compared).
Method: documentation only; no commands were run.
