---
id: computing-software.software-engineering.cobol.file-control-select
name: file-control-select
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, file-control-select, select, assign, organization, access-mode, file-status, file-control]
level: practitioner
status: docs-checked
description: "Declare files in FILE-CONTROL with the right organization, access mode, key and file status."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
  - https://gnucobol.sourceforge.io/doc/gnucobol.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SELECT, ASSIGN, ORGANIZATION, ACCESS MODE and FILE STATUS
**Goal:** map a logical COBOL file to a physical dataset or file. IBM rules are from the Enterprise COBOL for z/OS 6.4 Language Reference; GnuCOBOL rules from its Programmer's Guide.

```cobol
INPUT-OUTPUT SECTION.
FILE-CONTROL.
    SELECT CUST-FILE ASSIGN TO CUSTMAST
        ORGANIZATION IS INDEXED
        ACCESS MODE IS DYNAMIC
        RECORD KEY IS CUST-ID
        ALTERNATE RECORD KEY IS CUST-NAME WITH DUPLICATES
        FILE STATUS IS WS-FS.
    SELECT TRANS-FILE ASSIGN TO TRANSIN
        ORGANIZATION IS SEQUENTIAL.
```
- `SELECT`: the file name needs an FD or SD in the DATA DIVISION, must contain a letter and be unique in the program. `SELECT OPTIONAL` is for input, I-O or extend files that may be absent at run time.
- `ASSIGN TO name` (Enterprise COBOL): `name` is the DD name from the JCL, or an environment variable name if no file is allocated under that ddname. It is 1 to 8 characters, starts with a letter, has no underscore, and is folded to upper case. An optional `label-` prefix is documentation only; for QSAM files the `S-` field may be omitted, for VSAM sequential files `AS-` must be specified, and for VSAM indexed and relative files the organization field must be omitted. If an environment variable has no valid PATH or DSN option, or dynamic allocation fails, OPEN returns file status 98.
- `ASSIGN TO` (GnuCOBOL): the target may be a literal file name, a variable holding the name, or an environment variable (`ASSIGN TO EXTERNAL`). With the `filename-mapping` setting on (as in the default configuration), `ASSIGN TO "DATAFILE"` resolves to the value of `DD_DATAFILE`, then `dd_DATAFILE`, then `DATAFILE`, then the literal. `COB_FILE_PATH` sets the default directory for data files.
- ORGANIZATION: SEQUENTIAL (the default if omitted), LINE SEQUENTIAL (printable characters only), INDEXED, RELATIVE. The organization is fixed when the file is created.
- INDEXED files need a prime `RECORD KEY` (unique, not changeable on update) and may have `ALTERNATE RECORD KEY` clauses; indexed files must be on direct-access storage.
- ACCESS MODE: SEQUENTIAL (assumed if omitted, valid for all organizations), RANDOM or DYNAMIC (indexed and relative only; DYNAMIC allows both sequential and random statements).
- FILE STATUS: name a two-character alphanumeric or national item, or a two-digit DISPLAY/NATIONAL numeric item (no `P` in the picture), in WORKING-STORAGE, LOCAL-STORAGE or LINKAGE, and test it after every I/O. In the IBM manual's table, high-order digit 3 (permanent error) with low-order digit 5 (OPEN INPUT, I-O or EXTEND on a nonoptional file that was unavailable) gives status 35.

## Gotchas
- Status `00`-class values are successful; `02` means success with a duplicate alternate key, `05` means an optional file was unavailable at OPEN, `10`-class is end of file, `22` duplicate key, `23` record not found, `3x` permanent errors.
- The FILE STATUS value is set before any declarative, INVALID KEY or AT END handling runs.

## Self-check
Deliberately open a missing nonoptional file for input and confirm WS-FS holds a 3x status (35 on IBM) that you handle.

## Checked
2026-11-08. Confirmed against the Enterprise COBOL for z/OS 6.4 Language Reference PDF (SELECT, ASSIGN, ORGANIZATION, ACCESS MODE, FILE STATUS clauses and the file status key table) and the GnuCOBOL Programmer's Guide (SELECT ASSIGN TO section, filename-mapping, COB_FILE_PATH). Removed: the "UT-S-" prefix remark, the claim that a missing FILE STATUS makes an I/O error abend, and the 8-character DD name gotcha restated elsewhere.
Method: documentation only; no commands were run.
