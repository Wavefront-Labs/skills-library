---
id: computing-software.software-engineering.cobol.open-close-modes
name: open-close-modes
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, open-close-modes, cobol-sequential-files, open-input-output, open-extend, close-file]
level: intro
status: docs-checked
description: "Open and close files in the right mode and understand what each mode allows."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OPEN INPUT, OUTPUT, I-O, EXTEND and CLOSE
**Goal:** correct lifecycle for every file (Enterprise COBOL for z/OS 6.4 wording).

```cobol
OPEN INPUT  IN-FILE
     OUTPUT OUT-FILE
     EXTEND LOG-FILE
IF WS-FS-IN NOT = '00' PERFORM OPEN-FAILED END-IF
...
CLOSE IN-FILE OUT-FILE LOG-FILE
```
- INPUT permits input. OUTPUT permits output and can create the file; an existing file with records is replaced (for VSAM the data set must be defined reusable and have no alternate index). EXTEND appends after the last record, or creates the file. I-O permits both and only for direct-access devices; I-O is not valid for line-sequential files.
- Statements by open mode, sequential files: READ in INPUT and I-O; WRITE in OUTPUT and EXTEND; REWRITE in I-O. Indexed/relative files have a larger table (Table 50 of the manual).
- Phrases can appear in any order; files in one OPEN need not share organization.
- Availability (Table 48): INPUT, I-O or EXTEND on a missing file is unsuccessful (status 35); with `SELECT OPTIONAL`, INPUT opens normally (status 05, and the first read gives AT END), and I-O or EXTEND creates the file (status 05). OUTPUT on a missing file creates it.
- OPEN on an already open file is a logic error (status 41) and runs the file's EXCEPTION/ERROR procedure if specified; CLOSE on a file not open gives 42.
- A later OPEN of the same file must be preceded by a successful CLOSE (without REEL/UNIT or LOCK). After CLOSE the record area is not available.
- `CLOSE WITH LOCK` stops the file being opened again during this run (status 38 on a later OPEN).
- OPEN EXTEND on a sequential file requires new data in ascending sequence; OPEN does not read the first record.

## Gotchas
- With a FILE STATUS clause the status is updated by OPEN and CLOSE; check it after OPEN, not just after READ.
- Data can be moved to or from the record area only while the file is open.
- Status 37 means the file does not support the open mode requested; 39 means the program's fixed file attributes conflict with the file.

## Self-check
Open a nonexistent file for INPUT with and without OPTIONAL in a test; by Table 48 expect 35 and 05 respectively (the manual's rule; not run here).

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the OPEN statement section (formats, general rules, notes, Tables 48 to 51), the CLOSE statement section and Table 34, file status key values. Confirmed all claims above. Removed: "CLOSE flushes buffers; an unclosed output file may lose data on abnormal end" (not stated), "OPEN OUTPUT erases it (z/OS DISP=OLD/NEW also matters)" (JCL not read), "read and rewrite (or read/write for indexed/relative)" for I-O (replaced by the manual's table), and the unread ISO, ibm.com/docs root and GnuCOBOL sources.
Method: documentation only; no commands were run.
