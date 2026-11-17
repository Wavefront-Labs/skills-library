---
id: computing-software.software-engineering.cobol.evaluate-statement
name: evaluate-statement
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, evaluate-statement, cobol-conditions, evaluate-true, evaluate-also, when-other]
level: practitioner
status: gated
description: "Replace nested IFs with EVALUATE: value lists, ranges, EVALUATE TRUE and ALSO for multiple subjects."
sources:
  - https://www.iso.org/
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EVALUATE (multi-way branch)
**Goal:** express decision tables flatly.

```cobol
EVALUATE TRUE
    WHEN WS-AGE < 18        MOVE 'MINOR'  TO WS-CLASS
    WHEN WS-AGE < 65        MOVE 'ADULT'  TO WS-CLASS
    WHEN OTHER              MOVE 'SENIOR' TO WS-CLASS
END-EVALUATE

EVALUATE WS-TYPE ALSO WS-REGION
    WHEN 'A' ALSO 'N'  ...
    WHEN 'B' THRU 'D' ALSO ANY ...
END-EVALUATE
```
- Only the first matching WHEN runs, then control leaves the statement (no fall through). (gated: unconfirmed, source is paywalled or blocked)
- `WHEN OTHER` is the default; `ANY` matches anything; `THRU` ranges are inclusive.

## Gotchas
- Without WHEN OTHER an unexpected value silently does nothing.
- Order WHENs most specific first.

## Self-check
Feed boundary ages 17, 18, 64, 65; verify each lands in the intended class.

## Checked
2026-11-02. Confirmed: IBM Enterprise COBOL EVALUATE page confirms ALSO, THRU and ANY only; ISO text is paywalled.
Gated: whole skill; verify in IBM Enterprise COBOL Language Reference / ISO 1989.
Method: documentation only; no commands were run.
