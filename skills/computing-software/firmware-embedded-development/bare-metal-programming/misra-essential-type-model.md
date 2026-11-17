---
id: computing-software.firmware-embedded-development.bare-metal-programming.misra-essential-type-model
name: misra-essential-type-model
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [essential-type-model, misra-c, misra-c-2012, rule-10, implicit-conversion, composite-expression, essential-type, safety-critical, firmware-embedded-development]
level: advanced
status: draft
description: "Apply the MISRA C:2012 essential type model (Rules 10.1-10.8): essential type categories, composite expressions, widening casts, and rewriting typical violations."
sources:
  - https://www.misra.org.uk/misra-c/
  - https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite
  - https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MISRA C essential type model

**Goal:** write arithmetic that is MISRA C:2012 Rule 10.x compliant, which in practice
means no surprising implicit conversions, sign changes or narrowing.

## Essential type categories
Every expression has an essential type, ignoring C's integer promotion:
| Category | Examples |
|---|---|
| Boolean | result of `==`, `&&`, `!`; `bool` |
| character | `char` used for text |
| signed | `int8_t`, `int32_t`, signed literals |
| unsigned | `uint8_t`, `uint32_t`, `10U` |
| enum | each named enum type is its own category |
| floating | `float`, `double` |
`uint8_t a, b; a + b` has essential type `uint8_t` (C promotes to `int`, MISRA tracks
the narrower unsigned type). Integer constants take the smallest type that fits
(signed: STLR, unsigned: UTLR).

## The rules in one line each
- **10.1** operands must have an appropriate essential type (no arithmetic on Boolean,
  no bitwise/shift on signed, no `enum` arithmetic).
- **10.2** character arithmetic only in limited forms (`'0' + digit`).
- **10.3** no assignment to a narrower type or different category (`uint8_t x = u32;`).
- **10.4** both operands of an arithmetic/compare operator share a category (no
  `int32_t + uint32_t`).
- **10.5** casts must be appropriate (no cast of Boolean to int, no int to enum).
- **10.6** a composite expression must not be assigned to a wider type.
- **10.7** if a composite expression is an operand of an operator with a wider other
  operand, cast the composite first.
- **10.8** a composite expression must not be cast to a wider type or different category.

## Typical fixes
```c
uint16_t a, b; uint32_t r;
r = a * b;                    /* 10.6: composite uint16 assigned to uint32; also overflow risk */
r = (uint32_t)a * b;          /* compliant: widen an operand, not the result */

uint32_t mask = 1 << 31;      /* 10.1/UB: shifting signed int */
uint32_t mask = 1UL << 31U;   /* compliant */

int32_t s; uint32_t u;
if (s < u) {}                 /* 10.4: signed vs unsigned */
if ((s >= 0) && ((uint32_t)s < u)) {}

bool ok = (x & FLAG);         /* 10.3/14.4: not essentially Boolean */
bool ok = ((x & FLAG) != 0U);
```
- Use `U` suffix on unsigned constants everywhere; it fixes most 10.4 findings.
- Casting the **operand** before an operation (widen) is compliant; casting the **result
  of a composite expression** to a wider type (10.8) is the trap that hides overflow.

## Gotchas
- `uint8_t` shifts: `u8 << 4` is fine for the model but the result is computed in `int`;
  assigning back to `uint8_t` needs no cast if it fits essential rules, but think about
  lost bits.
- Enum constants used as array sizes or bit masks are flagged; use `#define` or
  `static const` unsigned values, or anonymous enums (treated as signed constants).
- Tools differ slightly; read the tool's rule notes, not just the rule headline.

## Verify
- [ ] Static analyser reports zero Rule 10.x violations or each has a deviation record.
- [ ] Code reviewed for intent: every explicit cast documented by why it is safe.
