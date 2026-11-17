---
id: computing-software.software-engineering.cobol.size-error-rounded
name: size-error-rounded
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, size-error-rounded, cobol-arithmetic, on-size-error, rounded-clause, arithmetic-overflow]
level: practitioner
status: docs-checked
description: "Trap overflow and divide-by-zero with ON SIZE ERROR and control rounding with ROUNDED."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ON SIZE ERROR and ROUNDED
**Goal:** never silently lose digits in money arithmetic (Enterprise COBOL for z/OS 6.4 wording).

```cobol
COMPUTE WS-TOTAL ROUNDED = WS-A * WS-B
    ON SIZE ERROR
        PERFORM OVERFLOW-ROUTINE
    NOT ON SIZE ERROR
        PERFORM POST-TOTAL
END-COMPUTE
```
- A size error occurs when the absolute value of the result, after decimal point alignment, exceeds the largest value the result field can hold; on division by zero; and in the exponentiation cases below.
- With ON SIZE ERROR and a size error, the affected receiver is not altered; the ON SIZE ERROR imperative runs and NOT ON SIZE ERROR is ignored. Without a size error, NOT ON SIZE ERROR runs.
- Without ON SIZE ERROR, truncation rules apply and the value of the receiver is still computed.
- Without ROUNDED, excess fraction digits are truncated. With ROUNDED, the least significant digit of the receiver is increased by 1 when the most significant excess digit is 5 or more. In floating-point arithmetic ROUNDED has no effect (the result is always rounded).
- If ROUNDED is given, rounding happens before the size error check.
- For a BINARY/COMP/COMP-4/COMP-5 receiver with ON SIZE ERROR, the limit is the value implied by its PICTURE, whatever the TRUNC option.

## Gotchas
- Size error applies only to final results, not intermediate results.
- In ADD CORRESPONDING and SUBTRACT CORRESPONDING, ON SIZE ERROR is not executed until all the individual additions or subtractions have completed.
- Exponentiation: `0 ** 0` runs the SIZE ERROR imperative if present, otherwise the value 1 is returned and a message issued; zero raised to a negative number runs it, otherwise the program ends abnormally; a negative base to a fractional power runs it, otherwise the absolute value of the base is used and a message issued.
- With ARITH(EXTEND), ROUNDED is not supported for receivers with 31 digit positions to the right of the decimal point (such as `PIC V31`).

## Self-check
Add 1 to a `PIC 9` item holding 9 with and without ON SIZE ERROR; only the guarded version leaves the item at 9.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the sections ROUNDED phrase, SIZE ERROR phrases (including Table 32, exponentiation size errors) and Arithmetic statements. Confirmed every claim above. Removed: the ROUNDED MODE IS NEAREST-EVEN/TRUNCATION/AWAY-FROM-ZERO claim (the 6.4 Language Reference has no such phrase), "modulo-wrapped depending on TRUNC" (the PDF states only that truncation rules apply), "ROUNDED rounds half away from zero" (replaced by IBM's own wording), the multi-receiver ADD claim (the PDF says receivers get the same computed temporary result in left-to-right order), and the unread ISO, ibm.com/docs root and GnuCOBOL sources.
Method: documentation only; no commands were run.
