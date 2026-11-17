---
id: computing-software.software-engineering.cobol.if-else-continue
name: if-else-continue
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, if-else-continue, cobol-control-flow, if-else-end-if, scope-terminators, next-sentence]
level: intro
status: docs-checked
description: "Write IF statements with explicit END-IF and use CONTINUE rather than NEXT SENTENCE."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IF/ELSE, CONTINUE, NEXT SENTENCE and scope terminators
**Goal:** avoid period-driven control flow bugs (Enterprise COBOL for z/OS 6.4 wording).

```cobol
IF WS-A > WS-B
    IF WS-C = 0
        CONTINUE
    ELSE
        PERFORM FIX-IT
    END-IF
ELSE
    PERFORM OTHER
END-IF.
```
- `CONTINUE` is a no-operation statement.
- `NEXT SENTENCE` transfers control to an implicit CONTINUE right after the next separator period. When it is written with END-IF, control does not go to the statement after END-IF but to the one after the closest following period.
- An IF's scope ends at an END-IF at the same nesting level, at a separator period, or (if nested) at an ELSE of an enclosing IF. END-IF lets an IF sit inside another conditional statement.
- statement-1 and statement-2 can be imperative, conditional, or an imperative followed by a conditional statement.
- Nested ELSE matches the nearest preceding IF not already matched with an ELSE or terminated; END-IF matches the nearest unterminated IF.
- With no ELSE, all statements between the condition and the matching END-IF or period belong to statement-1.
- Other explicit terminators seen in the manual: END-PERFORM, END-SEARCH, END-DELETE.

## Gotchas
- A separator period ends the IF (all open nested IFs), so a stray period mid-paragraph changes the logic.
- `ELSE NEXT SENTENCE` goes to just before the next period.

## Self-check
Search the source for `NEXT SENTENCE`; each hit should be justified or replaced with CONTINUE plus END-IF.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the IF statement section (NEXT SENTENCE, END-IF, transferring control, nested IF) and the CONTINUE statement section. Confirmed all claims above. Removed: "every IF, EVALUATE, PERFORM-inline, READ, SEARCH and CALL has an END- terminator" (only the terminators seen are listed), the compiler-option self-check (`-Wall`, FLAG(I): not in the sources read), and the unread ISO, ibm.com/docs root and GnuCOBOL sources.
Method: documentation only; no commands were run.
