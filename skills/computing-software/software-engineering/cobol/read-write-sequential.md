---
id: computing-software.software-engineering.cobol.read-write-sequential
name: read-write-sequential
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, read-write-sequential, cobol-sequential-files, read-at-end, write-from, priming-read]
level: practitioner
status: docs-checked
description: "Process a sequential file with the priming-read loop pattern and READ INTO / WRITE FROM."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# READ INTO, AT END, WRITE FROM and priming read
**Goal:** the canonical read loop (Enterprise COBOL for z/OS rules).

```cobol
READ IN-FILE INTO WS-IN-REC
    AT END SET AT-EOF TO TRUE
END-READ
PERFORM UNTIL AT-EOF
    PERFORM PROCESS-REC
    READ IN-FILE INTO WS-IN-REC
        AT END SET AT-EOF TO TRUE
    END-READ
END-PERFORM
...
WRITE OUT-REC FROM WS-OUT-REC
```
- READ names the file (`READ file-name`); WRITE names the record (`WRITE record-name`). Both must be defined by an FD entry.
- READ needs the file open in INPUT or I-O mode. WRITE to a sequential file needs OUTPUT or EXTEND.
- `READ ... INTO x` behaves as a READ followed by a MOVE of the current record to x (a group move when the FD has RECORD IS VARYING). The move does not happen if the READ was unsuccessful. The record stays available in both the record area and x. The record area and x must not be the same storage.
- `WRITE ... FROM x` behaves as `MOVE x TO record-name` then `WRITE record-name`; x is still available afterwards.
- NEXT RECORD is optional for sequential access and has no effect.
- At end: the I-O status gets the at-end value, the AT END imperative runs if coded (an applicable USE AFTER EXCEPTION declarative is then not run; with no AT END phrase it is run instead), the record area is undefined, and on QSAM files touching it can cause a protection exception.
- AT END can be omitted when an applicable EXCEPTION/ERROR procedure exists, or even when neither exists.

## Gotchas
- Sequential READ at end sets file status 10. An end-of-file condition is status class 1x; invalid key is 2x, permanent error 3x, logic error 4x. Hard I/O errors (3x, 9x) do not take AT END, so test FILE STATUS (or have a declarative) as well as coding AT END.
- A further READ after an at-end or failed read gives status 46 (no valid next record). READ on a file not open for input gives 47; WRITE on a file not open for output gives 48.
- If a record is shorter than the FD minimum or longer than its maximum, the READ succeeds and status is 04 under VLR(STANDARD) or 00 under VLR(COMPAT).
- An INVALID KEY phrase is not allowed for sequential files; use AT END or a declarative.

## Self-check
Process a 3-record file and an empty file; the loop body should run 3 and 0 times.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted): READ statement (formats, INTO rules, AT END condition, sequential access), WRITE statement (formats, FROM, file open modes), the File status key table, and the Invalid key condition. Rewrote claims to match them. Removed the unsupported claim that WRITE FROM on a closed or failed file corrupts the run, and the claim that INTO uses the actual length for variable records (the PDF states a group move when RECORD IS VARYING). Removed the unread ISO, ibm.com/docs and GnuCOBOL sources.
Method: documentation only; no commands were run.
