---
id: computing-software.software-engineering.assembly.asm-switch-lowering
name: asm-switch-lowering
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, asm-switch-lowering, asm-data-patterns]
level: practitioner
status: draft
description: "Lower switch and range checks into compact assembly: single-compare range tests, bit-set membership, lookup tables and when to prefer jump tables."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Lowering switch and if chains
**Goal:** translate multi-way decisions into short branch-light code.

- Unsigned range test: `c >= '0' && c <= '9'` becomes subtract then one unsigned compare.
```nasm
; is_digit(edi)
lea  eax, [rdi - '0']
cmp  eax, 9
setbe al                  ; unsigned <= 9 covers both bounds
movzx eax, al
ret
```
- Case-insensitive letter test: `(c | 0x20) - 'a' <= 25`.
```nasm
mov  eax, edi
or   eax, 0x20
sub  eax, 'a'
cmp  eax, 25
setbe al
```
- Set membership in a 64-value range with a bit mask:
```nasm
; true if edi in {'a','e','i','o','u'} (lowercase)
lea  ecx, [rdi - 'a']
cmp  ecx, 25
ja   .no
mov  eax, 0x104111           ; bits for a(0) e(4) i(8) o(14) u(20)
bt   eax, ecx
setc al
```
- Dense small-integer switches use a jump table (see jump-tables); sparse ones use binary search over case values; a pure value mapping uses a lookup table indexed by the input.
- Order `if` chains by frequency when they must stay branches; compilers choose among these automatically at -O2, so check their output first.

## Gotchas
- Check the bit mask arithmetic (a=0, e=4, i=8, o=14, u=20: 0x1 + 0x10 + 0x100 + 0x4000 + 0x100000 = 0x104111).
- Signed inputs need the unsigned trick applied to the correct width.

## Self-check
Write `is_hex_digit` with two range checks and test all 256 byte values.
