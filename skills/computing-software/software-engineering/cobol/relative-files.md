---
id: computing-software.software-engineering.cobol.relative-files
name: relative-files
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, relative-files, cobol-indexed-relative, relative-file, relative-key, rrds]
level: advanced
status: docs-checked
description: "Use RELATIVE organization where the record number is the key (RRDS on z/OS)."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RELATIVE files and RELATIVE KEY
**Goal:** direct access by record slot (Enterprise COBOL for z/OS rules).

```cobol
SELECT SLOTS ASSIGN TO SLOTDD
    ORGANIZATION IS RELATIVE
    ACCESS MODE IS RANDOM
    RELATIVE KEY IS WS-SLOT.
...
MOVE 42 TO WS-SLOT
READ SLOTS INVALID KEY PERFORM EMPTY-SLOT END-READ
```
- Think of the file as a string of record areas, each addressed by its relative record number; the first is 1 and the tenth is 10. Physical write order has no bearing on a record's number. Relative files must be direct-access files, with fixed or variable length records.
- RELATIVE KEY must be an unsigned integer item with no PICTURE symbol P, and it must not be in a record description of the file (it is not part of the record).
- RELATIVE KEY is always required for ACCESS RANDOM and DYNAMIC. For ACCESS SEQUENTIAL it is required only if you use START. A value placed in it for a sequential read without START is ignored and processing begins at the first record.
- All three access modes are allowed. Sequential access returns existing records in ascending relative record number; a successful sequential READ updates the RELATIVE KEY item to the number of the record returned.
- Random READ takes the number from the RELATIVE KEY item; if no such record exists, the INVALID KEY condition holds. The KEY IS phrase of READ must not be specified for relative files.
- WRITE: the INVALID KEY condition holds when the RELATIVE KEY names a record that already exists (random or dynamic access), when writing beyond the file's externally defined boundary, or when the relative record number has more significant digits than the key item. Status 22 means a duplicate key on a relative file; 23 means the random record does not exist; 24 is a boundary violation.
- DELETE removes the record; the slot is then available for a new record with the same RELATIVE KEY value. In sequential access the previous statement must be a successful READ and INVALID KEY must not be specified.
- REWRITE and WRITE may change the record length for relative files. REWRITE in random or dynamic mode uses the RELATIVE KEY item; a missing record gives invalid key.

## Gotchas
- A START on a relative file compares against the RELATIVE KEY item with numeric comparison rules; the KEY phrase, if given, must name the RELATIVE KEY.
- If a record is no longer accessible (deleted) after the position was set, a sequential READ moves to the next existing record.
- Choosing RELATIVE for sparse, widely spread keys is a design judgement; the Language Reference does not give a size rule, so check your data set definition before choosing.

## Self-check
Write slots 1, 5 and 9 and read sequentially; exactly three records come back with RELATIVE KEY 1, 5, 9.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted): ORGANIZATION clause and Relative organization, ACCESS MODE clause and the access-mode table, RELATIVE KEY clause, READ (relative sections), WRITE INVALID KEY cases, REWRITE and DELETE (relative sections), START (relative files) and the File status key table. Removed the unsupported "sequential reads skip empty slots" phrasing in favour of the documented "existing records" wording, the "file does not shrink" claim, and the dense-versus-sparse advice. Removed the unread ISO, ibm.com/docs and GnuCOBOL sources.
Method: documentation only; no commands were run.
