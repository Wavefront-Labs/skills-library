---
id: computing-software.software-engineering.assembly.got-plt-pic
name: got-plt-pic
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, got-plt-pic, asm-linking]
level: advanced
status: docs-checked
description: "GOT and PLT references from NASM ELF code (wrt ..plt, ..got, ..gotpc, ..gotoff) and the ld -z lazy, now and relro options that affect binding."
sources:
  - https://www.nasm.us/doc/nasm09.html
  - https://sourceware.org/binutils/docs/ld/Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GOT, PLT and PIC
**Goal:** reference external symbols from position-independent assembly.

- ELF has no segment-base references, so NASM's `elf` formats reuse the `WRT` operator for PIC relocation types: `..gotpc`, `..gotoff`, `..got`, `..plt` and `..sym`.
```nasm
extern printf
call  printf wrt ..plt        ; linker builds a PLT entry for the symbol
```
- `wrt ..plt` makes the linker build a procedure linkage table entry; use it only where a PC-relative relocation is generated normally (the destination of `call` or `jmp`), because ELF has no relocation to refer to PLT entries absolutely.
- `wrt ..got` on an external or global symbol makes the linker build a GOT entry holding the symbol's address; the reference gives the distance from the beginning of the GOT to that entry, so add the GOT address, load from it, and you get the symbol's address.
- `wrt ..gotpc` gives the distance from the current section to the GOT (symbol `_GLOBAL_OFFSET_TABLE_`; add `$$` for the real address). `wrt ..gotoff` gives the distance from the GOT to a location in your own sections. `wrt ..sym` writes a relocation aimed directly at the symbol.
- Thread-local access in ELF64 uses `wrt ..gottpoff`, for example `mov rax,[rel tid wrt ..gottpoff]` followed by an `fs:` load.
- Linker options (ld `-z`): `lazy` marks the output so function resolution is deferred to the first call, and lazy binding is the default; `now` asks the dynamic linker to resolve all symbols at startup or `dlopen`. `relro` creates a `PT_GNU_RELRO` segment that should be made read-only after relocation (`norelro` omits it). `ibtplt` generates IBT-enabled PLT entries (Linux/i386 and x86_64).

## Gotchas
- `wrt ..plt` cannot be used for data references.
- `relro` protection is ineffective if `common-page-size` is smaller than the system page size.

## Self-check
Assemble a call with `wrt ..plt`, link against libc, and confirm with `objdump -dr` that the call targets a PLT stub.

## Checked
Method: docs-checked 2026-11-09 against NASM manual chapter 9 (section 9.10.3 ELF special symbols and WRT, TLS section) and the ld options page (-z keywords lazy, now, relro, ibtplt). Dropped the GAS and AArch64 snippets, the full-RELRO hardening claim, the `.plt.sec` and scratch-register statements, and interposition advice, which these pages do not confirm.
