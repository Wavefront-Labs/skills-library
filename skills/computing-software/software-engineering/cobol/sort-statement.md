---
id: computing-software.software-engineering.cobol.sort-statement
name: sort-statement
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, sort-statement, cobol-sort-merge, sort-using-giving, sort-keys, sd-entry]
level: practitioner
status: docs-checked
description: "Sort files with the SORT statement, SD work file, ASCENDING/DESCENDING keys and USING/GIVING."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SORT with USING and GIVING
**Goal:** sort in-program without external steps (Enterprise COBOL for z/OS 6.4 wording).

```cobol
SD SORT-WORK.
01 SORT-REC.
   05 SR-DEPT PIC X(4).
   05 SR-NAME PIC X(20).
...
SORT SORT-WORK
    ON ASCENDING KEY SR-DEPT
    ON DESCENDING KEY SR-NAME
    WITH DUPLICATES IN ORDER
    USING IN-FILE
    GIVING OUT-FILE
```
- file-name-1 is the file named in the SD entry. Format 1 can appear anywhere in the PROCEDURE DIVISION except in declaratives, and is not supported with the THREAD option.
- USING files and GIVING files must not be open when the SORT runs. The sort opens, reads (or writes) and closes them. GIVING output is written as if by OPEN OUTPUT, WRITE with no options and CLOSE; all must have FD entries.
- Keys are listed from left to right in decreasing significance, whatever the ASCENDING/DESCENDING grouping. A key must sit in the same position and format in each input file, cannot have or be under an OCCURS, cannot be variably located, DBCS, national decimal or a dynamic-length item. With variable-length records, keys must lie within the minimum record size.
- If the GIVING file is indexed, the first key must be ASCENDING and occupy the same positions as its prime record key.
- `WITH DUPLICATES IN ORDER`: records with equal keys come back in input-file order (and in release order when an input procedure is used). Without it the order is undefined.
- `COLLATING SEQUENCE alphabet-name` applies to alphabetic, alphanumeric, alphanumeric-edited, external floating-point and numeric-edited keys. If omitted, the OBJECT-COMPUTER PROGRAM COLLATING SEQUENCE is used, else EBCDIC.
- SORT-RETURN holds 0 (successful) or 16 (unsuccessful) after the sort; if it is unsuccessful and the program never references SORT-RETURN, a message is displayed.
- Format 2 `SORT table-name ON ASCENDING KEY key...` sorts the elements of a table in place (the table needs OCCURS; the rightmost subscript, if any, must be omitted or ALL). The KEY phrase can be left out only when the OCCURS clause has a KEY phrase. Format 2 works with THREAD and SORT-RETURN does not apply.

## Gotchas
- Where sort control and SORT special registers (SORT-CORE-SIZE and others) overlap, values in the sort control file take precedence over the special registers.
- An input procedure must not run MERGE, RETURN or a format 1 SORT; an output procedure must not run MERGE, RELEASE or a format 1 SORT (see the sort-input-output-procedures skill).
- For SORTWKnn DD statements and z/OS sort job settings, use the Programming Guide and JCL manuals (not read here).

## Self-check
Sort a small file with duplicate keys using DUPLICATES IN ORDER and check equal-key records keep their input order.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the SORT statement section (formats 1 and 2, KEY, DUPLICATES, COLLATING SEQUENCE, USING, GIVING, special registers) and the SORT-RETURN special register. Confirmed all claims above. Removed: "SORT-RETURN checked after the SORT (0 = success)" now reworded to IBM's 0/16, "GnuCOBOL and IBM support DUPLICATES IN ORDER", "z/OS needs SORTWKnn DD statements or dynamic allocation; GnuCOBOL uses temp files" (Programming Guide and GnuCOBOL docs, not read), the SELECT line in the example, "COMP-3 keys work only on valid packed data", and the unread ISO, ibm.com/docs root and GnuCOBOL sources.
Method: documentation only; no commands were run.
