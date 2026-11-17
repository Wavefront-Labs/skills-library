---
id: computing-software.software-engineering.cobol.line-sequential
name: line-sequential
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, line-sequential, cobol-sequential-files, line-sequential-files, text-file-io, trailing-spaces]
level: practitioner
status: docs-checked
description: "Read and write newline-delimited text files with ORGANIZATION LINE SEQUENTIAL and handle trailing spaces."
sources:
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
  - https://gnucobol.sourceforge.io/doc/gnucobol.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LINE SEQUENTIAL text files (GnuCOBOL)
**Goal:** exchange text files with other tools.
```cobol
SELECT TXT-FILE ASSIGN TO 'data.txt'
    ORGANIZATION IS LINE SEQUENTIAL.
FD TXT-FILE.
01 TXT-REC PIC X(200).
```
- Records end with an end-of-record delimiter: X'0A' on Unix-style builds, X'0D0A' on native Windows builds. Fixed- and variable-length record formats are supported.
- On READ, a record shorter than the record description is padded with spaces to the right.
- Longer records: the Programmer's Guide says excess data is truncated; the runtime setting `COB_LS_SPLIT` (default true in current runtime.cfg) instead returns the rest as further records with status 06, and with it false the record is truncated with status 04.
- `COB_LS_FIXED` makes records fixed length instead of stripping trailing spaces (useful before REWRITE); `COB_LS_VALIDATE` (default true) validates data on read (status 09) and write (status 71).
- Do not put COMP or BINARY fields in the record: their bytes could look like an end-of-record delimiter.
- This is the only ORGANIZATION valid for a file assigned to the PRINTER device.

## Gotchas
- Reading a Windows file on Unix leaves the carriage return in the record unless the runtime strips it; check your data.

## Self-check
Write three lines with trailing spaces, then list the file size; compare with and without `COB_LS_FIXED`.

## Checked
2026-11-02. Checked against the GnuCOBOL Programmer's Guide (ORGANIZATION LINE SEQUENTIAL) and runtime.cfg in the manual's runtime configuration appendix. Removed: all IBM Enterprise COBOL statements, the claim that GnuCOBOL trims trailing spaces by default (the setting is described only as the alternative to `COB_LS_FIXED`), and the `wc -c` check.

Method: documentation only; no commands were run.
