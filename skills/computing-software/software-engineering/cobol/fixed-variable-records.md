---
id: computing-software.software-engineering.cobol.fixed-variable-records
name: fixed-variable-records
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, fixed-variable-records, cobol-record-layouts, recording-mode, record-varying, rdw]
level: practitioner
status: docs-checked
description: "Describe fixed, variable and multi-layout records with RECORD CONTAINS, RECORD VARYING DEPENDING ON and RECORDING MODE in Enterprise COBOL."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fixed, variable and multi-format records
**Goal:** correct record handling for every file type (Enterprise COBOL for z/OS rules; JCL dataset attributes are outside this source).

- Record size is the number of bytes needed to store the record internally, whatever the USAGE of its items. Ten DBCS or ten national characters is `RECORD CONTAINS 20 CHARACTERS`.
- Format 1 `RECORD CONTAINS n CHARACTERS`: fixed length. `RECORD CONTAINS 0 CHARACTERS` is allowed for input QSAM files with fixed-length records; the size comes from the DD statement or data set label at run time, and it cannot be combined with SAME AREA, SAME RECORD AREA or APPLY WRITE-ONLY, nor used on an SD.
- Format 2 `RECORD CONTAINS min TO max CHARACTERS`: fixed or variable length; never required, since the compiler derives min and max from the 01 records.
- Format 3, variable length with a length field:
```cobol
FD IN-FILE RECORD VARYING FROM 10 TO 200 CHARACTERS
           DEPENDING ON WS-REC-LEN.
01 IN-REC PIC X(200).
```
  The DEPENDING ON item must be an elementary unsigned integer. Put the length in it before RELEASE, REWRITE or WRITE; after a successful READ it holds the length just read. DELETE, START, WRITE and an unsuccessful READ leave it unchanged.
- If RECORD is omitted, the compiler takes lengths from the record descriptions; with OCCURS DEPENDING ON it uses the maximum.
- RECORDING MODE (QSAM only; ignored for VSAM): F fixed (no length fields), V variable (each record has a record-length field and each block a block-descriptor field, each 4 bytes, supplied automatically and not available to your program), U one record per block with no length fields (cannot combine with BLOCK CONTAINS), S spanned (needs BLOCK CONTAINS CHARACTERS; not for ASCII files). With no clause the compiler picks F, V or S from the RECORD clause, record sizes and block size; U is never chosen by default.
- Multi-layout files: several 01 records under one FD share the same storage (they are implicitly redefined), and after a READ only the bytes within the current record's length are replaced. Decide the layout from a record-type field:
```cobol
EVALUATE IN-TYPE
    WHEN 'H' MOVE IN-REC TO HEADER-REC
    WHEN 'D' MOVE IN-REC TO DETAIL-REC
END-EVALUATE
```
- With READ INTO and several record descriptions that are not all alphanumeric, variable-length files get a group move and fixed-length files move from the largest record description (the first one if several tie).

## Gotchas
- A record shorter than the FD minimum leaves the right-hand part of the record area undefined; a longer one is truncated to the maximum. The READ still succeeds, with status 04 under VLR(STANDARD) or 00 under VLR(COMPAT).
- Writing or rewriting a record outside the RECORD IS VARYING limits, or rewriting a record to a different size where that is not allowed, gives status 44.
- The data set attributes (RECFM, LRECL, block size) must agree with the program; a conflict can fail OPEN with status 39.

## Self-check
Write a variable-length file with three different lengths and read back the lengths into a table.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted): RECORD clause (formats 1-3), RECORDING MODE clause, READ statement (multiple record descriptions, record length conflict), WRITE/REWRITE record-size notes and the File status key table. Removed the RECFM=FB/VB and LRECL = max + 4 rules, the GnuCOBOL no-RDW claim and the "reading VB as FB" advice, because they depend on z/OS JCL and GnuCOBOL documentation not read here. Removed the unread ibm.com/docs, z/OS and GnuCOBOL sources.
Method: documentation only; no commands were run.
