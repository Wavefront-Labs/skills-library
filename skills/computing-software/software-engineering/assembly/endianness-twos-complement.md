---
id: computing-software.software-engineering.assembly.endianness-twos-complement
name: endianness-twos-complement
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, endianness-twos-complement, asm-concepts]
level: intro
status: draft
description: "Byte order and signed integer representation on x86-64 and AArch64: little-endian layout, negation, sign extension and what flags report."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://developer.arm.com/documentation/ddi0487/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Endianness and two's complement
**Goal:** predict how multi-byte values sit in memory and how signed values behave in registers.

- x86-64 and AArch64 as used on Linux, Windows and macOS are little-endian: the least significant byte has the lowest address.
```nasm
mov dword [rel buf], 0x11223344   ; memory bytes: 44 33 22 11
mov al, [rel buf]                 ; al = 0x44
```
- Negation is invert-and-add-one: `-x == ~x + 1`. `neg eax` (x86) and `neg w0` (A64, alias of `sub w0, wzr, w0`) do this.
- Sign extension copies the top bit into the widened bits (`movsx`/`movsxd` on x86, `sxtb`/`sxth`/`sxtw` on A64). Zero extension fills with 0 (`movzx`, `uxtb`/`uxth`).
- The same bits are signed or unsigned by interpretation only; the CPU provides separate conditions (above/below vs greater/less).
- CF reports unsigned carry/borrow out of the top bit; OF reports signed overflow. 0x7FFFFFFF + 1 sets OF but not CF.

## Gotchas
- Network protocols are big-endian: convert with `bswap` (x86) or `rev` (A64).
- Reading a 4-byte field as 8 bytes also reads the neighbour; always match operand size to the field.
- AArch64 can run big-endian in principle but mainstream OS ABIs are little-endian.

## Self-check
Predict the byte order of a stored dword, then dump it in a debugger and compare.
