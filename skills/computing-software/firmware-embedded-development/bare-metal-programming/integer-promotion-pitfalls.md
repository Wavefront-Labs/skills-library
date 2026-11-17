---
id: computing-software.firmware-embedded-development.bare-metal-programming.integer-promotion-pitfalls
name: integer-promotion-pitfalls
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [integer-promotion, usual-arithmetic-conversions, undefined-behaviour, signed-overflow, shift-ub, ubsan, cert-c, embedded-c, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Avoid C integer promotion and undefined-behaviour traps in firmware: small types promoted to int, mixed signedness, oversize shifts, and catching them with GCC UBSan."
sources:
  - https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules
  - https://wiki.sei.cmu.edu/confluence/display/c/INT34-C.+Do+not+shift+an+expression+by+a+negative+number+of+bits+or+by+greater+than+or+equal+to+the+number+of+bits+that+exist+in+the+operand
  - https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integer promotion and undefined behaviour

**Goal:** recognise the handful of integer rules that cause real firmware bugs, and write
expressions whose result is the same at every optimisation level.

## Promotion: small types become int
SEI CERT INT02-C: integer types smaller than `int` are promoted when an operation is performed on
them. If all values of the original type fit in an `int` the value becomes an `int`; otherwise it
becomes an `unsigned int`. Promotion also applies to operands of unary `+`, `-` and `~` and to the
operands of the shift operators. So the width of `int` on your target decides the result.

```c
uint8_t port = 0x5a;
uint8_t bad  = (~port) >> 4;           /* ~port is an int (0xffffffa5 where int is 32 bits)  */
uint8_t good = (uint8_t)(~port) >> 4;  /* the SEI page's compliant form: 0x0a                */
```
The SEI page notes that whether the shifted value is negative is implementation-defined.

```c
unsigned short x = 45000, y = 50000;
unsigned int z_bad  = x * y;                 /* UB where short is 16 bits and int is 32 */
unsigned int z_good = x * (unsigned int)y;   /* multiplication is unsigned */
```
On those widths the `unsigned short` operands become signed `int`, and the product 2250000000
exceeds the largest signed 32-bit value, which is undefined behaviour (INT02-C).

## Usual arithmetic conversions: signed meets unsigned
After promotion, if the unsigned operand has rank greater than or equal to the signed operand's,
the signed operand is converted to unsigned (INT02-C).
```c
int si = -1; unsigned int ui = 1;
si < ui;                    /* 0: si becomes UINT_MAX */
si < (int)ui;               /* 1, correct only when ui is known to fit in an int */
(si < 0 || (unsigned)si < ui);   /* the SEI page's general form */
```

## Shifts (INT34-C)
- The result has the type of the promoted left operand.
- If the right operand is negative, or greater than or equal to the width of the promoted left
  operand, the behaviour is undefined. The SEI rule uses precision: guard shifts so the count is
  below the number of value bits.
- For a signed left operand, a negative value or a result that is not representable is undefined.
  CERT advises doing shifts and other bitwise operations on unsigned operands only.
- Signed overflow in general is undefined (INT02-C example above). Do the arithmetic in an unsigned
  type or check the range first.

## Catching it with GCC
- `-fsanitize=undefined` enables the undefined-behaviour checks; related options listed on the GCC
  page include `-fsanitize=shift` (with `shift-base` and `shift-exponent`) and
  `-fsanitize=signed-integer-overflow`. Run host unit tests of portable modules under it.
- `-fsanitize-trap=undefined` reports undefined behaviour with `__builtin_trap` instead of a
  libubsan routine, which avoids the runtime library; useful in test builds on target.
- `-ftrapv` also emits traps for signed overflow, whereas `-fsanitize=undefined` gives a
  diagnostic message.
- Static analysers cover many of these patterns; MISRA C:2012 Rules 10.1, 10.3, 10.4, 10.6, 10.7
  and 10.8 are listed by CERT as related to INT02-C.

## Verify
- [ ] Host unit tests run under `-fsanitize=undefined` with no reports.
- [ ] Every shift count is range-checked or provably below the operand width.
- [ ] Every mixed signed and unsigned comparison is written explicitly.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed on SEI CERT INT02-C and INT34-C and the GCC Instrumentation Options page: promotion rule, usual arithmetic conversion rule, the ~port and unsigned short examples, shift rules, sanitizer option names and the trap option, related MISRA rule list.
Removed because the pages do not state them: the 16-bit-int AVR example, `1 << 31` specifics, the pointer-overflow-check and uninitialised-variable rows, `-fwrapv` and `-fsanitize=integer`, HardFault behaviour, and warning-flag advice.
