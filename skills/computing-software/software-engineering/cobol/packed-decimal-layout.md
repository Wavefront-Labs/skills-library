---
id: computing-software.software-engineering.cobol.packed-decimal-layout
name: packed-decimal-layout
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, packed-decimal-layout, cobol-usage, packed-decimal-nibbles, comp-3, numeric-class-test, invalid-numeric-data]
level: advanced
status: docs-checked
description: "How PACKED-DECIMAL (COMP-3) stores digits and sign, its length limits, and how to guard packed fields with the NUMERIC test and INITIALIZE."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packed-decimal layout and guarding against invalid data
**Goal:** declare packed fields correctly and keep bad data out of arithmetic (Enterprise COBOL for z/OS rules).

- `PACKED-DECIMAL` and `COMP-3` (COMPUTATIONAL-3) are the same thing: an internal decimal item. Storage holds two digits per character position (byte), except the trailing position, which holds the low-order digit and the sign.
- Digits 0-9 plus a sign. Maximum 18 digits, or 31 when the ARITH(EXTEND) compiler option is in effect (ARITH(COMPAT) keeps 18).
- The sign uses the same 4-bit configuration as zoned decimal. The exact sign codes are documented in the Programming Guide ("Sign representation of zoned and packed-decimal data"), which this review did not read, so look the codes up there before hand-decoding dumps.
- Efficiency: the Language Reference says to define packed items with an odd number of digits so all bits are used (this also gives more efficient code). The `RULES(NOEVENPACK)` option flags even-digit packed items.
- The NUMERIC class test is valid for items of USAGE DISPLAY, NATIONAL, COMP-3 or PACKED-DECIMAL. Whether a sign is valid depends on the NUMCLS installation option and the NUMPROC compiler option. If the picture has an operational sign, only an elementary item with numeric contents and a valid sign tests NUMERIC.
- A NUMERIC test on an alphanumeric group is not allowed if the group contains signed elementary items, so test the packed elementary fields.
- NUMPROC and TRUNC affect how numeric items are used; sign tests and numeric comparisons depend on NUMPROC (and INVDATA for comparisons). Their exact effects are in the Programming Guide.
- Safe pattern:
```cobol
INITIALIZE WS-REC            *> numeric items to zero, alphanumeric to spaces
IF IN-AMT IS NUMERIC
    ADD IN-AMT TO WS-TOTAL
ELSE
    PERFORM REJECT-RECORD
END-IF
```
- INITIALIZE (no phrases) acts as implicit MOVEs: ZERO to numeric and numeric-edited receivers, SPACE to alphabetic, alphanumeric and similar receivers. It skips FILLER items and items under REDEFINES or RENAMES unless told otherwise (FILLER phrase for FILLER items).

## Gotchas
- A group MOVE of spaces or low-values into a record leaves packed fields holding bit patterns that are not valid packed data. Test with IS NUMERIC before arithmetic; the Language Reference does not name the runtime failure, so check your platform's messages.
- Reading a record straight into an unchecked packed field is the usual way bad data arrives; validate on input.

## Self-check
Feed a record with spaces in a packed field; confirm the program's NUMERIC test rejects it before any arithmetic.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted): USAGE clause (PACKED-DECIMAL, COMP-3, computational items, digit limits), class condition (NUMERIC rules), INITIALIZE statement and its rules. Removed the specific sign nibble values, the S0C7 abend claim, the NUMPROC(PFD) versus NOPFD behaviour and the GnuCOBOL claim, because the Language Reference defers those to the Programming Guide or does not cover them. Removed the unread ibm.com/docs and GnuCOBOL sources.
Method: documentation only; no commands were run.
