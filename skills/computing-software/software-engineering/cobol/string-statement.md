---
id: computing-software.software-engineering.cobol.string-statement
name: string-statement
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, string-statement, string-concatenation, delimited-by, with-pointer, on-overflow]
level: intro
status: docs-checked
description: "Concatenate fields into a target with STRING, delimiters, WITH POINTER and ON OVERFLOW."
sources:
  - https://www.ibm.com/docs/en/cobol-zos/6.4?topic=statements-string-statement
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STRING (concatenation) with DELIMITED BY and POINTER
**Goal:** build text safely (Enterprise COBOL for z/OS rules).

```cobol
MOVE SPACES TO WS-OUT
MOVE 1 TO WS-PTR
STRING FIRST-NAME DELIMITED BY SPACE
       ' '        DELIMITED BY SIZE
       LAST-NAME  DELIMITED BY SPACE
    INTO WS-OUT
    WITH POINTER WS-PTR
    ON OVERFLOW PERFORM TRUNCATED
END-STRING
```
- STRING does not pad the target: after it runs, only the part of the receiving field that was written changes and the rest keeps its previous data, so MOVE SPACES first.
- You must set the explicit pointer yourself, to a value of at least 1 and no more than the receiver's length; the pointer field must be large enough to hold the receiver length plus 1. At the end it is one past the last character transferred.
- `DELIMITED BY SIZE` transfers each whole sending field; `DELIMITED BY SPACE` (or another delimiter) stops before the delimiter, which is not transferred, so names with spaces get cut.
- The receiving field must not be numeric-edited, alphanumeric-edited, national-edited or external floating-point, and must not have the JUSTIFIED clause. Numeric sending items must be integers without P in the PICTURE.
- Without POINTER an implicit pointer starting at 1 is used.

## Gotchas
- ON OVERFLOW fires when the pointer is less than 1 or exceeds the length of the receiving field; no more data is transferred then and NOT ON OVERFLOW is ignored.
- Reuse of a previous result without clearing leaves stale trailing characters.
- The receiver and pointer must not overlap each other or any sending field: results are undefined.

## Self-check
Build "SMITH JOHN" from two names and verify the length with the pointer value minus 1.

## Checked
Date: 2026-11-08. Read the whole IBM docs STRING page and, in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted), the STRING statement Data flow section. Confirmed the no-padding rule, pointer initial value, size and final position, DELIMITED BY SIZE versus delimiter behaviour, the receiver restrictions, the overflow conditions and the overlap rule. Corrected the self-check (the example output has no comma, so the expected string is "SMITH JOHN"). Removed the unread ISO and GnuCOBOL root sources; GnuCOBOL behaviour is not covered.
Method: documentation only; no commands were run.
