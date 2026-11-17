---
id: computing-software.software-engineering.cobol.file-section-fd
name: file-section-fd
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, file-section-fd, cobol-storage-sections, file-section, fd-entry, block-contains-0, record-contains]
level: practitioner
status: docs-checked
description: "Describe file records with FD entries, RECORD and RECORDING MODE clauses, and let z/OS choose QSAM block sizes with BLOCK CONTAINS 0."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FILE SECTION, FD, RECORD CONTAINS and BLOCK CONTAINS
**Goal:** declare file layouts that match the physical dataset (Enterprise COBOL for z/OS 6.4).

```cobol
FILE SECTION.
FD  TRANS-FILE
    RECORDING MODE IS F
    BLOCK CONTAINS 0 RECORDS
    RECORD CONTAINS 80 CHARACTERS.
01  TRANS-REC.
    05 TR-TYPE PIC X.
    05 TR-DATA PIC X(79).
```
- The FILE SECTION header is followed by a period; each file needs an FD (sort/merge files need an SD instead). The file-name must match the SELECT clause and contain at least one alphabetic character. The last clause of the entry ends in a period; clauses after the file-name are optional and can come in any order.
- When more than one record description follows an FD, each is an alternative description of the same storage area.
- `BLOCK CONTAINS 0` is allowed for QSAM files: the block size is then determined at run time from the DD parameters or the data set label (for output, the system may choose a system-determined block size). The clause can be omitted for VSAM files (syntax checked, no effect), for SYSIN and SYSOUT files, and is ignored under an SD. When omitted for other files the compiler assumes unblocked records.
- `CHARACTERS` is the default unit for BLOCK CONTAINS and counts bytes, including control bytes and padding. RECORDS is the other unit.
- RECORD CONTAINS counts bytes regardless of USAGE: 10 DBCS or 10 national characters are `RECORD CONTAINS 20 CHARACTERS`.
- `RECORD CONTAINS 0 CHARACTERS` is allowed for input QSAM files of fixed-length records (size taken from the DD or label at run time); it cannot be used on an SD.
- Variable-length records: `RECORD CONTAINS 10 TO 200 CHARACTERS` or `RECORD VARYING FROM 10 TO 200 DEPENDING ON REC-LEN`. With DEPENDING ON, REC-LEN must be an elementary unsigned integer set to the byte count before WRITE, REWRITE or RELEASE, and holds the length after a successful READ or RETURN.
- `RECORDING MODE` (QSAM only, ignored for VSAM): F fixed, V variable (4-byte record-length and block-descriptor fields added automatically), U one record per block (cannot be used with BLOCK CONTAINS), S spanned (needs BLOCK CONTAINS CHARACTERS). If omitted, the compiler infers F or V from the RECORD clause and record sizes.
- LABEL RECORDS, VALUE OF and DATA RECORDS are syntax checked only and have no effect at run time.

## Gotchas
- A VALUE clause is not allowed in record descriptions in the FILE SECTION (it is for WORKING-STORAGE and LOCAL-STORAGE), except for condition-name (88) entries.
- Data areas in the FILE SECTION are not available for processing unless the file is open.
- For an external file, BLOCK CONTAINS and the maximum record size must agree across all FDs for that file in the run unit.

## Self-check
Open the file and READ a record; the file status is 00 and the record length (for example `LENGTH OF` the record or the DEPENDING ON item) matches the dataset's LRECL.

## Checked
2026-11-08. Confirmed against the Enterprise COBOL for z/OS 6.4 Language Reference (Chapter 24 FILE SECTION; Chapter 25 file description entry, BLOCK CONTAINS, RECORD, LABEL RECORDS, VALUE OF, DATA RECORDS, RECORDING MODE; VALUE clause in Chapter 26). Removed: the claim that a RECORD/LRECL mismatch gives a status 39 on OPEN and the status 04 self-check (file status behaviour is in the Programming Guide, not read), the "usual best practice" opinion, the "most compilers" and GnuCOBOL generalisations, and the ISO and GnuCOBOL sources.
Method: documentation only; no commands were run.
