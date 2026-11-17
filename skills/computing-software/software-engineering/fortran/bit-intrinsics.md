---
id: computing-software.software-engineering.fortran.bit-intrinsics
name: bit-intrinsics
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, bit-intrinsics, fortran-numeric-intrinsics]
level: practitioner
status: docs-checked
description: "Operate on bits with iand, ishft, ibset, btest, popcnt, leadz, trailz and the shift intrinsics."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bit manipulation intrinsics
**Goal:** manipulate bits portably.
```fortran
integer :: flags
flags = ibset(0, 3)                  ! bit 3 set
if (btest(flags, 3)) print *, 'set'
flags = iand(flags, not(ishft(1, 3)))
print *, popcnt(255), leadz(1), trailz(8)
```
- `btest(i, pos)` is true if the bit at `pos` is set; counting of bits starts at 0. `ibset(i, pos)` sets that bit to one.
- `shiftl(i, shift)` shifts left; `shift` must be nonnegative and at most `bit_size(i)`, otherwise the result is undefined. `shifta` shifts right with an arithmetic fill (sign bit). `shiftl` and `shifta` are Fortran 2008.
- `ishft(i, shift)` shifts left for a positive `shift` and right for a negative one; if `abs(shift)` is greater than `bit_size(i)` the value is undefined.
- `bit_size(i)` returns the number of bits of the type of `i`.
- `popcnt(i)` counts the set bits; `leadz(i)` and `trailz(i)` count leading and trailing zero bits, returning `bit_size(i)` if all bits are zero (Fortran 2008).
- `iand` is the standard bitwise AND; `and` is a GNU extension kept for backwards compatibility.
## Gotchas
- Shift counts outside the ranges above give undefined results.
## Self-check
Verify `popcnt(255)` equals 8.

## Checked
2026-11-02. Confirmed in intrinsic.texi: BTEST, IBSET, SHIFTL, SHIFTA, ISHFT, BIT_SIZE, POPCNT, LEADZ, TRAILZ, IAND, AND (GNU extension). Removed: 'ishft handles shifts >= bit_size' (the manual says undefined), signed-integer advice, printed values 8 31 3 (not stated).
Method: documentation only; no commands were run.
