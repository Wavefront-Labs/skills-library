---
id: computing-software.software-engineering.cobol.perform-forms
name: perform-forms
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, perform-forms, cobol-control-flow, perform-until, perform-varying, perform-thru, inline-perform]
level: intro
status: docs-checked
description: "Use the forms of PERFORM for loops and subroutines, including TEST BEFORE/AFTER and nested VARYING."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PERFORM: paragraph, THRU, TIMES, UNTIL, VARYING and inline
**Goal:** structure control flow with PERFORM (Enterprise COBOL for z/OS 6.4 wording).

```cobol
PERFORM INIT-PARA
PERFORM PARA-A THRU PARA-A-EXIT
PERFORM 3 TIMES ... END-PERFORM
PERFORM UNTIL AT-EOF
    PERFORM READ-NEXT
END-PERFORM
PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
    ...
END-PERFORM
PERFORM SCAN-CELL THRU SCAN-CELL-EXIT
        VARYING I FROM 1 BY 1 UNTIL I > R
        AFTER J FROM 1 BY 1 UNTIL J > C
```
- Out-of-line: names a procedure-name-1 (paragraph or section), optionally THRU procedure-name-2; control returns after the last statement of the paragraph (or last paragraph of the section) it names. Inline: no procedure-name, statements up to END-PERFORM. The two forms cannot be combined.
- With TIMES the count is an integer item or literal, up to 999,999,999. Zero or negative means the procedures are not run; changing the item after the PERFORM starts has no effect.
- UNTIL: the default is `WITH TEST BEFORE` (the condition is tested before each execution; if it is already true nothing runs). `WITH TEST AFTER` runs the statements at least once before the first test. `UNTIL EXIT` loops until you escape it (inline: EXIT PERFORM, not EXIT PERFORM CYCLE; out-of-line: GOBACK or STOP). EXIT PARAGRAPH and EXIT SECTION do not escape it, and it cannot be combined with TEST or VARYING.
- VARYING: items and literals are numeric; the BY value must be nonzero. For a nested `AFTER`, the inner identifier cycles completely each time the outer one is augmented, and the inner one is reset to its FROM value. The AFTER phrase must not be used on an inline PERFORM (procedure-name-1 omitted).
- `EXIT PERFORM` leaves an inline PERFORM without a GO TO.

## Gotchas
- A PERFORM must not cause itself to execute (recursive PERFORM gives unpredictable results).
- PERFORM ranges: an active PERFORM that starts inside another's range must not let control pass through the other's exit point; two active PERFORMs may share a common exit. If there are several paths to the return point, make procedure-name-2 a paragraph holding only EXIT and send all paths to it.
- After the loop the VARYING identifier holds a value that exceeds the last-used setting by the increment (so for `UNTIL I > N` step 1 it ends at N + 1). With AFTER, the inner identifier ends holding its FROM value.
- Subscripts in the UNTIL condition are re-evaluated each time the condition is tested.

## Self-check
Trace a VARYING loop that DISPLAYs I after the loop; the value is the bound plus one step.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the PERFORM statement section (formats 1 to 4, UNTIL EXIT note, varying one to three identifiers, varying rules) and the EXIT statement section (EXIT PERFORM, EXIT PARAGRAPH, EXIT SECTION). Confirmed all claims above. Removed: "the index is incremented before the test on each pass" (IBM describes augmenting after the procedures are executed), "the standard disallows overlapping ranges" (replaced by IBM's rule), and the unread ISO, ibm.com/docs root and GnuCOBOL sources.
Method: documentation only; no commands were run.
