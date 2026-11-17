---
id: computing-software.software-engineering.cobol.sort-input-output-procedures
name: sort-input-output-procedures
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, sort-input-output-procedures, cobol-sort-merge, sort-input-procedure, release-record, return-statement]
level: advanced
status: docs-checked
description: "Filter or transform records around a sort with INPUT PROCEDURE (RELEASE) and OUTPUT PROCEDURE (RETURN)."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SORT INPUT PROCEDURE, OUTPUT PROCEDURE, RELEASE and RETURN
**Goal:** process while sorting without intermediate files (Enterprise COBOL for z/OS 6.4 wording).

```cobol
SORT SORT-WORK ON ASCENDING KEY SR-DEPT
    INPUT PROCEDURE IS 1000-SELECT
    OUTPUT PROCEDURE IS 2000-REPORT.
...
1000-SELECT SECTION.
    PERFORM UNTIL AT-EOF
        READ IN-FILE AT END SET AT-EOF TO TRUE
        NOT AT END
            IF IN-ACTIVE
                RELEASE SORT-REC FROM IN-REC
            END-IF
        END-READ
    END-PERFORM.
2000-REPORT SECTION.
    RETURN SORT-WORK AT END SET SORT-DONE TO TRUE END-RETURN
    PERFORM UNTIL SORT-DONE ...
```
- INPUT PROCEDURE selects, modifies or copies records and passes them one at a time with RELEASE to the SD file. OUTPUT PROCEDURE receives them in sorted order with RETURN. You open and close any other files yourself.
- procedure-name-1 THRU procedure-name-2 name the first and last section or paragraph. The range includes statements reached through CALL, EXIT, GO TO, PERFORM and XML PARSE, and declaratives triggered from it.
- The procedures work like a basic PERFORM: execution ends after the last statement, which can be EXIT. The compiler adds the return mechanism.
- RELEASE `record-name [FROM identifier]`: record-name is a record in the SD; only inside an INPUT PROCEDURE of a SORT, at least one RELEASE is required. FROM is a MOVE then RELEASE; identifier and record must not share storage. After a plain RELEASE the record area is no longer available (unless SAME RECORD AREA).
- RETURN `sd-file RECORD [INTO identifier] AT END ... [NOT AT END ...] END-RETURN`: only inside an OUTPUT PROCEDURE of a SORT or MERGE; at least one RETURN is required. AT END runs after all records have been returned, and no further RETURN may be executed in that procedure.
- With several record descriptions for the SD they share storage; after RETURN only the current record is available.

## Gotchas
- The input procedure must not run MERGE, RETURN or a format 1 SORT; the output procedure must not run MERGE, RELEASE or a format 1 SORT.
- Control passes to the output procedure only after the records have been sequenced; the sort is terminated when the output procedure ends.
- A RELEASE or RETURN in a nested program cannot be for a SORT or MERGE in the containing program.
- Setting SORT-RETURN to 16 in an error declarative or input/output procedure ends the sort or merge at the next input or output function for it.

## Self-check
Filter half the records in the input procedure; the output record count must equal the filtered count.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the SORT statement (INPUT PROCEDURE and OUTPUT PROCEDURE phrases), RELEASE statement, RETURN statement and SORT-RETURN sections. Confirmed all claims above. Removed: "do not GO TO out of a procedure; it must run to its end" (IBM says GO TO transfers are part of the range, so it is not forbidden outright), "do not RELEASE after the sort has begun returning" (IBM's rule is that the output procedure must not run RELEASE), and the unread ISO, ibm.com/docs root and GnuCOBOL sources.
Method: documentation only; no commands were run.
