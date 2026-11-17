---
id: computing-software.software-engineering.cobol.go-to-alter
name: go-to-alter
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, go-to-alter, cobol-control-flow, go-to-depending, alter-statement, legacy-control-flow]
level: practitioner
status: docs-checked
description: "Read and tame legacy GO TO and ALTER code; recognize GO TO DEPENDING as a computed branch."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GO TO, GO TO DEPENDING ON and ALTER
**Goal:** maintain old code without breaking it (Enterprise COBOL for z/OS 6.4 wording).

```cobol
GO TO P1 P2 P3 DEPENDING ON WS-CODE.
...
P-EXIT. EXIT.
```
- `GO TO ... DEPENDING ON n`: identifier is an integer numeric elementary item; 1 goes to the first name, 2 to the second, and so on, up to 255 names. A value outside 1 through the number of names means no transfer: control continues with the next statement.
- `ALTER para TO [PROCEED TO] other` changes the GO TO in paragraph `para`. That paragraph must contain only one sentence: a GO TO without DEPENDING ON. After the ALTER executes, reaching `para` sends control to `other`. IBM says ALTER encourages unstructured programming and EVALUATE gives the same function; with LP(64) a diagnostic is issued for ALTER.
- Statements after an unconditional GO TO in the same sentence are not executed.
- An altered GO TO that has not yet been ALTERed acts like CONTINUE.

## Gotchas
- ALTER cannot be used in RECURSIVE programs, in methods, or in programs compiled with THREAD. In an INITIAL program the altered GO TOs are reset on each entry.
- Several active PERFORMs may share an exit, but an active PERFORM must not let control pass through the exit point of another active PERFORM, so a GO TO out of a performed range can break the return.
- Where several logical paths reach the return point, IBM suggests making procedure-name-2 of the PERFORM an EXIT-only paragraph and sending all paths to it.

## Self-check
Replace one ALTER'd switch with a flag and EVALUATE in a copy of the program and compare outputs on a regression file.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the GO TO statement (unconditional, conditional, altered), ALTER statement and PERFORM statement (overlapping range rule, EXIT paragraph) sections. Confirmed all claims above. Removed: "ALTER removed from newer standards" (not stated), "ALTER makes static analysis impossible" and "the same paragraph runs different code depending on history" as unsupported prose (IBM states only the structured-programming concern and that ALTER acts as a switch), and the unread ISO and ibm.com/docs root sources.
Method: documentation only; no commands were run.
