---
id: computing-software.software-engineering.cobol.print-control
name: print-control
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, print-control, cobol-report, write-advancing, page-heading, carriage-control, linage]
level: practitioner
status: docs-checked
description: "Format print files with WRITE ADVANCING, LINAGE and END-OF-PAGE, and know when carriage control characters are added."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WRITE AFTER/BEFORE ADVANCING, LINAGE and carriage control
**Goal:** paginated listings without Report Writer (Enterprise COBOL for z/OS rules).

```cobol
WRITE PRT-REC FROM HEAD-1 AFTER ADVANCING PAGE
WRITE PRT-REC FROM DETAIL-LINE AFTER ADVANCING 1 LINE
ADD 1 TO WS-LINE-CNT
IF WS-LINE-CNT > 55
    PERFORM PRINT-HEADINGS
END-IF
```
- `AFTER` or `BEFORE ADVANCING` takes identifier-2 (an integer item), an integer, PAGE, or a mnemonic-name. AFTER advances, then prints; BEFORE prints, then advances. The count may be zero. mnemonic-name must be equated to an environment-name in SPECIAL-NAMES and gives a skip to channels 1 through 12 or space suppression.
- Omitting ADVANCING gives automatic single spacing, as if `AFTER ADVANCING 1 LINE`.
- PAGE with no meaning for the device falls back to ADVANCING 1 LINE. With a LINAGE clause it repositions to the first printable line of the next page; without LINAGE, to line 1 of the next page.
- A LINAGE clause in the FD gives you a logical page: body lines, optional `WITH FOOTING AT`, `LINES AT TOP` and `LINES AT BOTTOM` (margins default to zero, footing defaults to the page body size). It applies to sequential files opened OUTPUT or EXTEND. The special register LINAGE-COUNTER is reset to 1 by ADVANCING PAGE and when a new page starts, and otherwise grows by the lines advanced (1 if ADVANCING is omitted).
- `AT END-OF-PAGE` (or EOP) requires a LINAGE clause and runs after the WRITE once the footing area is reached. If a WRITE cannot fit in the page body, automatic page overflow moves to the next page first. Neither BEFORE/AFTER ADVANCING nor AT END-OF-PAGE is supported for VSAM files.
- ADVANCING, or a LINAGE clause, makes the compiler generate a carriage control character in the record. With the ADV compiler option the compiler adds 1 byte to the record length for it; if your record already reserves its first byte for control, use NOADV (no effect for LINAGE files, which are handled as if ADV were set).
- Without LINAGE, you track lines yourself with a counter such as `WS-LINE-CNT`, as in the example.

## Gotchas
- If the file is EXTERNAL and none of its connectors has LINAGE, then if any program in the run unit uses WRITE with ADVANCING, all programs with a WRITE must use ADVANCING.
- Line-sequential files do not support WRITE BEFORE ADVANCING, AT END-OF-PAGE, mnemonic-name ADVANCING or a LINAGE clause (AFTER ADVANCING with an integer, identifier or PAGE is allowed).
- The DD attributes needed for spool printing (record format with control characters, LRECL allowing the extra byte) are z/OS JCL matters outside this source; check them in the JCL reference.

## Self-check
Print 120 lines with LINAGE 60 and confirm LINAGE-COUNTER resets and the heading appears on each new page.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted): WRITE statement (ADVANCING phrase rules, LINAGE-COUNTER rules, ADV/NOADV note, END-OF-PAGE phrases), LINAGE clause, and the line-sequential unsupported-clause list. Removed the claim that mixing WRITE with and without ADVANCING is disallowed generally (the PDF restricts it only for EXTERNAL files with no LINAGE) and the RECFM=FBA/ASA spool claims (z/OS JCL, not read). Removed the unread ibm.com/docs and GnuCOBOL sources.
Method: documentation only; no commands were run.
