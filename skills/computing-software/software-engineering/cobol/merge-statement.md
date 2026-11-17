---
id: computing-software.software-engineering.cobol.merge-statement
name: merge-statement
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, merge-statement, cobol-sort-merge, merge-using-giving]
level: advanced
status: docs-checked
description: "Combine two or more already-sorted files with MERGE."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MERGE of pre-sorted files
**Goal:** merge sorted inputs without a full sort (Enterprise COBOL for z/OS 6.4 wording).

```cobol
MERGE MRG-WORK ON ASCENDING KEY MR-KEY
    USING FILE-A FILE-B FILE-C
    GIVING MERGED-FILE
```
- MERGE combines two or more files already sorted in an identical sequence on the same keys and makes the records available to an output procedure or output file.
- The format has USING with OUTPUT PROCEDURE or GIVING; there is no INPUT PROCEDURE. RETURN is used inside the OUTPUT PROCEDURE.
- file-name-1 is the SD file describing the records; no file-name may be repeated in the statement.
- The merge key must be in the same position and format in each input file. Keys are listed left to right in decreasing significance and have the same restrictions as SORT keys (no OCCURS, not variably located, not DBCS, not national decimal).
- Input and output files must have sequential or dynamic access mode and FD entries, and must not be open when MERGE runs; MERGE opens, reads or writes, and closes them.
- MERGE can appear anywhere in the PROCEDURE DIVISION except in declaratives and is not supported with the THREAD option.
- COLLATING SEQUENCE: as for SORT (program collating sequence if omitted, else EBCDIC).

## Gotchas
- The output procedure must not run MERGE, RELEASE or a format 1 SORT.
- The SORT-RETURN special register is 0 or 16 at completion, as for SORT.
- Record sizes of input files must fit the SD record description (see USING phrase).
- For z/OS work-space allocation see the Programming Guide (not read here).

## Self-check
Merge two small sorted files and check the output is ordered and holds the sum of the record counts.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the MERGE statement section in full, RETURN statement and SORT-RETURN. Confirmed all claims above. Removed: "unsorted inputs produce out-of-order output with no diagnostic" (not stated), "z/OS: the merge work space comes from SORTWK DDs" (Programming Guide, not read), and the unread ISO, ibm.com/docs root and GnuCOBOL sources.
Method: documentation only; no commands were run.
