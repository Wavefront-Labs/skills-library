---
id: computing-software.software-engineering.cobol.on-exception-handlers
name: on-exception-handlers
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, on-exception-handlers, cobol-exceptions, invalid-key, on-exception, on-overflow]
level: practitioner
status: docs-checked
description: "Attach the right conditional phrase to each statement and combine with NOT phrases."
sources:
  - https://www.iso.org/
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AT END, INVALID KEY, ON EXCEPTION, ON OVERFLOW
**Goal:** handle expected failures where they occur.

| Statement | Phrase |
|---|---|
| READ (sequential) | AT END / NOT AT END |
| RETURN (sort/merge) | AT END / NOT AT END |
| READ/WRITE/REWRITE/DELETE/START on keyed files | INVALID KEY / NOT INVALID KEY |
| WRITE (printer files) | AT END-OF-PAGE / NOT AT END-OF-PAGE |
| CALL | ON EXCEPTION / NOT ON EXCEPTION (ON OVERFLOW has the same effect) |
| STRING/UNSTRING | ON OVERFLOW / NOT ON OVERFLOW |
| JSON/XML GENERATE and PARSE | ON EXCEPTION / NOT ON EXCEPTION |
| ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE | ON SIZE ERROR / NOT ON SIZE ERROR |
```cobol
WRITE CUST-REC
    INVALID KEY PERFORM DUP-KEY
    NOT INVALID KEY ADD 1 TO WS-WRITTEN
END-WRITE
```
- Order on an invalid key condition: the FILE STATUS item is set first; then the INVALID KEY imperative statement runs if coded (any EXCEPTION/ERROR declarative for the file is not executed); if not coded, an applicable declarative runs.
- A CALL exception occurs when the called subprogram cannot be made available (or a Java exception for a Java static method call). With ON EXCEPTION coded, control goes to its statement; NOT ON EXCEPTION runs after a successful return.
- Without ON SIZE ERROR, truncation rules apply and the receiver is updated; with it, the receiver is left unaltered and the phrase's statement runs (NOT ON SIZE ERROR is then ignored).

## Gotchas
- If you code INVALID KEY, only invalid key conditions go to it (file status 2x); other file errors follow the USE declarative rules, so keep FILE STATUS.
- INVALID KEY must not be specified for a sequential-organization file.
- A statement with a conditional phrase is only an imperative statement if closed by its END- scope terminator, so add END-READ, END-CALL and so on when more code follows in the same sentence.
- Enterprise COBOL 6.4 lists no ON EXCEPTION phrase for ACCEPT or DISPLAY.

## Self-check
Write a duplicate prime key to an indexed file and verify the INVALID KEY branch runs and the file status is 22.

## Checked
2026-11-08: confirmed against the Enterprise COBOL for z/OS 6.4 Language Reference: the imperative and conditional statement lists (Procedure division structure), Invalid key condition, File status key table (status 22 for a duplicate prime key), CALL ON EXCEPTION and ON OVERFLOW, SIZE ERROR phrases, and the INVALID KEY rules for sequential files. Removed the ACCEPT/DISPLAY ON EXCEPTION row (not in the 6.4 lists) and the unsupported "abends or continues" sentence. GnuCOBOL behaviour was not checked.
Method: documentation only; no commands were run.
