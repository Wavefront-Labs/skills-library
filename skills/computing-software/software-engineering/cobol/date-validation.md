---
id: computing-software.software-engineering.cobol.date-validation
name: date-validation
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, date-validation, cobol-dates, leap-year-check, integer-of-date-roundtrip]
level: practitioner
status: draft
description: "Validate calendar dates with an INTEGER-OF-DATE round trip or an explicit month/leap-year table."
sources:
  - https://www.iso.org/
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Validating dates and leap years
**Goal:** reject 2025-02-30 reliably.

```cobol
COMPUTE WS-INT = FUNCTION INTEGER-OF-DATE(WS-YYYYMMDD)
IF WS-INT = 0
    SET DATE-INVALID TO TRUE
ELSE
    IF FUNCTION DATE-OF-INTEGER(WS-INT) NOT = WS-YYYYMMDD
        SET DATE-INVALID TO TRUE
    END-IF
END-IF
```
- Some compilers abend (rather than return 0) on a badly out-of-range argument; test numeric class and month 1-12 first.
- Manual alternative: month table of days, February 29 allowed when year divisible by 4 and not by 100, or divisible by 400.
- IBM Language Environment provides CEEDAYS to validate and convert Lilian dates (callable service; arguments per LE docs, verify before use).

## Gotchas
- Valid-looking `20250230` can pass a regexish format check; always validate semantically.
- Never trust a zero date `00000000` as "no date" without a documented convention.

## Self-check
Run 20240229 (valid) and 20230229 (invalid) through the routine.
