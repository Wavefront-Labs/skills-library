---
id: computing-software.software-engineering.cobol.file-status-codes
name: file-status-codes
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, file-status-codes, cobol-sequential-files, file-status-00, file-status-35, io-status-checking]
level: practitioner
status: docs-checked
description: "Decode the two-character FILE STATUS values of Enterprise COBOL for z/OS and build a standard status-check paragraph."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FILE STATUS codes and what they mean
**Goal:** diagnose I/O faults quickly (Enterprise COBOL for z/OS 6.4 table; other compilers may differ).

The FILE STATUS data item can be a 2-character alphanumeric or national item, or a 2-digit DISPLAY or NATIONAL numeric item, defined in WORKING-STORAGE, LOCAL-STORAGE or LINKAGE. It is set after every I/O operation on the file, before any declarative, INVALID KEY or AT END processing runs.

| Code | Meaning |
|---|---|
| 00 | successful, no further information |
| 02 | success, duplicate key detected (indexed files with alternate keys that allow duplicates) |
| 04 | READ succeeded but the record was shorter than the minimum or longer than the maximum for the FD (you get 00 instead under VLR(COMPAT)) |
| 05 | OPEN succeeded but the referenced OPTIONAL file was unavailable |
| 07 | CLOSE/OPEN with NO REWIND, REEL/UNIT or FOR REMOVAL on a non-reel/unit medium |
| 10 | at end: no next record, or first READ on an unavailable optional file |
| 14 | sequential READ of a relative file whose relative record number has too many digits for the key item |
| 21 | sequence error on a sequentially accessed indexed file (prime key changed before REWRITE, or ascending order violated) |
| 22 | duplicate key (relative file WRITE; indexed prime or alternate key without DUPLICATES) |
| 23 | random access of a record that does not exist (or START/random READ on an unavailable optional file) |
| 24 | write beyond the file's boundaries (relative or indexed), or relative record number too large for the key item |
| 30 | permanent error, no further information |
| 34 | permanent error: boundary violation writing a sequential file |
| 35 | OPEN INPUT, I-O or EXTEND on a nonoptional file that was unavailable |
| 37 | OPEN mode not supported by the file |
| 38 | OPEN on a file previously closed with lock |
| 39 | OPEN failed: conflict between file attributes and the program (organization, keys, code set, record size, record type, blocking) |
| 41 | OPEN of a file that is already open |
| 42 | CLOSE of a file that is not open |
| 43 | REWRITE (or DELETE on keyed files) not preceded by a successful READ in sequential access |
| 44 | REWRITE with a different record size, or record outside the RECORD IS VARYING limits |
| 46 | sequential READ with no valid next record (previous READ failed or hit end) |
| 47 | READ on a file not open INPUT or I-O |
| 48 | WRITE on a file not open I-O, OUTPUT or EXTEND |
| 49 | DELETE or REWRITE on a file not open I-O |
| 9x | implementor defined; see below |

```cobol
CHECK-STATUS.
    IF WS-FS NOT = '00' AND NOT = '10'
        DISPLAY 'I/O ERROR ' WS-FS ' ON ' WS-FILE-NAME
        MOVE 16 TO RETURN-CODE
        GOBACK
    END-IF.
```
- For VSAM files you can add a second item, a 6-byte alphanumeric group (WORKING-STORAGE or LINKAGE), as `FILE STATUS IS fs vsam-code`: 2 bytes VSAM return code, 2 bytes function code, 2 bytes feedback code, all binary. It does not apply to QSAM files and is only meaningful when the return code is nonzero.

## Gotchas
- First digit classes: 0 successful completion, 1 at end, 2 invalid key, 3 permanent error, 4 logic error, 9 implementor defined.
- 9x: 90 depends (VSAM return codes, or none for QSAM; multithreaded CLOSE on the wrong thread), 91 VSAM password failure, 92 logic error, 93 resource unavailable (not QSAM), 95 invalid or incomplete file information (not QSAM), 96 missing DD for an OPEN OUTPUT (or I-O/EXTEND on an optional file), 97 VSAM OPEN verified (00 instead if VSAMOPENFS(SUCC) is on), 98 open failed from an invalid environment variable in ASSIGN or a dynamic allocation failure.
- A QSAM abend during READ, WRITE or REWRITE can give 34 or 90 while an error declarative is active.

## Self-check
Force 35 and 10 by opening a missing nonoptional file and reading to end of file; confirm your paragraph reports 35 and ignores 10.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted): File status key section and Table 34 (all rows listed above), the FILE STATUS clause (data-name-1 and the 6-byte data-name-8), and the USE EXCEPTION/ERROR declarative note on codes 34 and 90. Corrected 05 (optional file unavailable at OPEN, not "not present"), 35 (nonoptional file unavailable), 39 (attribute conflict, wider than RECFM/LRECL), 47/48/49 (individually described) and added the missing rows. Removed the claim that ISO and GnuCOBOL agree with these codes, the FD-level self-check for 39 (not run) and the unread ISO, ibm.com/docs and GnuCOBOL sources.
Method: documentation only; no commands were run.
