---
id: computing-software.software-engineering.cobol.numval-conversion
name: numval-conversion
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, numval-conversion, cobol-intrinsic, function-numval, function-numval-c, test-numval]
level: practitioner
status: docs-checked
description: "Convert text to numbers safely with NUMVAL and validate with TEST-NUMVAL first."
sources:
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NUMVAL, NUMVAL-C and TEST-NUMVAL
**Goal:** parse user or file text into numerics safely.
```cobol
IF FUNCTION TEST-NUMVAL(WS-TEXT) = 0
    COMPUTE WS-AMT = FUNCTION NUMVAL(WS-TEXT)
ELSE
    PERFORM BAD-NUMBER
END-IF
COMPUTE WS-PRICE = FUNCTION NUMVAL-C(WS-PRICE-TXT)
```
- `NUMVAL(string)` accepts `#`, `-#`, `+#`, `#-`, `#+`, `#CR` and `#DB`, where `#` is digits (with a decimal point).
- `TEST-NUMVAL(string)` returns 0 when the string is acceptable to NUMVAL; otherwise the position of the first bad character, or the field length plus one for cases such as all spaces. A zero-length, all-space or incomplete string (such as `+.`) is an error.
- `NUMVAL-C(string [, symbol] [, LOCALE locale-name] [, ANYCASE])` ignores the currency string and grouping separators before the decimal separator.
- `NUMVAL-F` converts floating-point text.
- Alphanumeric items must be converted with these functions before use in arithmetic.

## Gotchas
- Always call `TEST-NUMVAL` first; do not assume NUMVAL rejects bad text.

## Self-check
Run `TEST-NUMVAL` on `'12.5'`, `'12.5x'` and `' -7 '` on your build and compare with the Guide's rules.

## Checked
2026-11-02. Checked against the GnuCOBOL Programmer's Guide function entries NUMVAL, NUMVAL-C, TEST-NUMVAL and the Literals section. Removed: the claim that NUMVAL returns 0 for invalid text, the DECIMAL-POINT IS COMMA remark, the IBM release remark, and the predicted values 0, 5, 0.

Method: documentation only; no commands were run.
