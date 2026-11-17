---
id: computing-software.software-engineering.cobol.usage-display-comp
name: usage-display-comp
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, usage-display-comp, cobol-usage, comp-3, packed-decimal, binary-usage, comp-5]
level: practitioner
status: docs-checked
description: "Choose the USAGE for each numeric field: DISPLAY, BINARY/COMP, packed COMP-3, native COMP-5 or floating COMP-1/COMP-2."
sources:
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
  - https://gnucobol.sourceforge.io/doc/gnucobol.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# USAGE DISPLAY, BINARY, COMP, COMP-3, COMP-5, COMP-1 and COMP-2 (GnuCOBOL)
**Goal:** pick a representation for correctness, interchange and speed.
- `DISPLAY`: one character per digit; readable.
- `BINARY` / `COMP` (also `COMP-4`): binary integer sized from the PICTURE per the `binary-size` config option (default `1-2-4-8` in default.conf: 1-2 digits 1 byte, 3-4 digits 2 bytes, 5-9 digits 4 bytes, 10-18 digits 8 bytes). `-fibmcomp` sets `binary-size=2-4-8`. Byte order defaults to big-endian; `binary-byteorder: native` stores native order (more efficient on little-endian machines).
- `COMP-3` / `PACKED-DECIMAL`: two digits per byte; the last byte's right nibble is always a sign (D is negative, other values positive per the Guide's tests). The first byte has an unused left nibble when the PICTURE has an even number of 9s; `PIC S9(3) COMP-3` holding -15 is stored as hex `015D`.
- `COMP-5`: native binary integer; range depends on the number of 9s and `binary-size`. `COMP-X`: native binary, unsigned for PIC X.
- `COMP-1` / `COMP-2`: same as `FLOAT-SHORT` / `FLOAT-LONG`, IEEE 754 binary32 / binary64 in native byte order. `FLOAT-DECIMAL-16` / `-34` are IEEE 754 Decimal64 / Decimal128.
- `USAGE NATIONAL` is syntactically recognized but not supported.
- A USAGE on a group item applies to subordinate items that have none of their own.
```cobol
01 WS-QTY   PIC S9(4)      COMP.
01 WS-AMT   PIC S9(7)V99   COMP-3.
01 WS-HANDLE PIC S9(9)     COMP-5.
```

## Gotchas
- DISPLAY, PACKED-DECIMAL, COMP-5 and COMP-X items without `S` in the PICTURE (or any item marked UNSIGNED) strip the sign and keep the absolute value.
- Floating point cannot represent every decimal fraction exactly; use packed or DISPLAY decimal for money.

## Self-check
Store -15 in `PIC S9(3) COMP-3`, hex dump the field and expect `015D`.

## Checked
2026-11-02. Checked against the GnuCOBOL Programmer's Guide USAGE section and the manual (Optimize binary), and default.conf binary-size and binary-byteorder. Removed: IBM z/OS statements (hex float, FLOAT(IEEE), TRUNC behaviour), the big-endian-on-IBM remark, the generic size formula for COMP-3 (not stated), and claims about EBCDIC conversion. Corrected: the old binary size table (1-4 digits = 2 bytes) is the `2-4-8` setting; the GnuCOBOL default is `1-2-4-8`.

Method: documentation only; no commands were run.
