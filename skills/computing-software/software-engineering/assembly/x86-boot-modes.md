---
id: computing-software.software-engineering.assembly.x86-boot-modes
name: x86-boot-modes
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, x86-boot-modes, asm-baremetal]
level: sme
status: draft
description: "x86 boot basics: BIOS boot sector at 0x7C00 in real mode, a NASM boot sector example, and the sequence to reach 64-bit long mode."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://www.nasm.us/doc/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# x86 real mode and long mode transition
**Goal:** boot your own code and know the path to 64-bit mode.

```nasm
; boot.asm -> nasm -f bin boot.asm -o boot.bin ; qemu-system-x86_64 -drive format=raw,file=boot.bin
bits 16
org 0x7c00
start:
    cli
    xor  ax, ax
    mov  ds, ax
    mov  ss, ax
    mov  sp, 0x7c00
    mov  si, msg
.next:
    lodsb
    test al, al
    jz   .halt
    mov  ah, 0x0e              ; BIOS teletype
    mov  bx, 0x0007
    int  0x10
    jmp  .next
.halt:
    hlt
    jmp  .halt
msg: db "boot ok", 0
times 510 - ($ - $$) db 0
dw 0xaa55                      ; boot signature
```
- Legacy BIOS loads the first 512-byte sector to `0x7C00` and jumps to it in 16-bit real mode if bytes 510-511 are `55 AA`.
- Sequence to long mode: enable the A20 line, load a GDT (`lgdt`), set CR0.PE to enter protected mode and far-jump to reload CS, build page tables, set CR4.PAE, set EFER.LME (MSR `0xC0000080` bit 8), set CR0.PG to enable paging, then far-jump into a 64-bit code segment.
- Modern PCs boot through UEFI, which starts programs already in 64-bit mode and passes services via the firmware tables; legacy BIOS boot is still available in emulators and some firmware.
- Exact register and descriptor layouts are in Intel SDM volume 3.

## Gotchas
- Real-mode code uses 16-bit default operand and address sizes (`bits 16`); wrong `bits` directives produce garbage encodings.
- The BIOS may leave the segment registers in unspecified states; set them explicitly.

## Self-check
Boot the sample in QEMU and see "boot ok", then add a `jmp $` loop at the end and a debugger breakpoint at 0x7c00.
