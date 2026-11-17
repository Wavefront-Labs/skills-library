---
id: computing-software.software-engineering.cobol.control-break-processing
name: control-break-processing
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, control-break-processing, cobol-batch-patterns, control-break, group-totals, sorted-input-report]
level: practitioner
status: draft
description: "Implement subtotal and total logic over sorted input by detecting key changes."
sources:
  - https://www.iso.org/
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Control-break (group totals) processing
**Goal:** correct group totals with first and last group handled.

```cobol
PERFORM READ-NEXT
MOVE IN-DEPT TO WS-PREV-DEPT
PERFORM UNTIL AT-EOF
    IF IN-DEPT NOT = WS-PREV-DEPT
        PERFORM PRINT-DEPT-TOTAL
        MOVE IN-DEPT TO WS-PREV-DEPT
        MOVE ZERO TO WS-DEPT-TOTAL
    END-IF
    ADD IN-AMT TO WS-DEPT-TOTAL WS-GRAND-TOTAL
    PERFORM READ-NEXT
END-PERFORM
PERFORM PRINT-DEPT-TOTAL
PERFORM PRINT-GRAND-TOTAL
```
- Input must be sorted by the control key (multi-level breaks: test highest-level key first and cascade).
- The final group total prints after the loop; empty input prints no groups.
- Check ordering: abend or reject if a key is lower than the previous.

## Gotchas
- Forgetting to reset the accumulator after the break.
- Comparing the new key before `WS-PREV` is initialized (first record).

## Self-check
Test with one group, many groups, and empty input.
