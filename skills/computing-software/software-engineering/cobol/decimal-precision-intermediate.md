---
id: computing-software.software-engineering.cobol.decimal-precision-intermediate
name: decimal-precision-intermediate
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, decimal-precision-intermediate, cobol-arithmetic, arith-extend, trunc-option, intermediate-results]
level: advanced
status: draft
description: "Understand compiler-specific intermediate precision, TRUNC(STD/OPT/BIN) and ARITH(COMPAT/EXTEND) effects on arithmetic."
sources:
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Intermediate results, TRUNC and ARITH options
**Goal:** get the same answer across builds and platforms.

- IBM `ARITH(COMPAT)`: up to 18 digits in intermediates; `ARITH(EXTEND)`: up to 31 digits for fields and intermediates.
- IBM `TRUNC(STD)`: binary fields are truncated to the PICTURE digits (correct but slower); `TRUNC(OPT)`: compiler may use full storage range (fast, wrong if values exceed PICTURE); `TRUNC(BIN)`: binary fields hold the full binary range.
- GnuCOBOL: `-fbinary-truncate` (default on) is the analogue; `-fnotrunc` disables truncation (names per `cobc --help`; verify).
- Use one common copybook of compiler options for the whole shop and document it.

## Gotchas
- Moving between platforms with different truncation defaults changes results only when a value exceeds the PICTURE; test with boundary values.
- Floating (COMP-1/2) intermediates appear if you use `**` with non-integer exponents.

## Self-check
Run a boundary test (9999 + 1 into `S9(4) COMP`) under each option set and record results in the project notes.
