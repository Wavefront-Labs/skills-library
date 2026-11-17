---
id: computing-software.software-engineering.cobol.cics-file-control
name: cics-file-control
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, cics-file-control, cobol-cics, cics-read-update, cics-startbr, resp-resp2, cics-handle-condition]
level: advanced
status: draft
description: "Access VSAM files through CICS file control and test RESP/RESP2 instead of HANDLE CONDITION."
sources:
  - https://www.ibm.com/docs/en/cics-ts
  - https://www.ibm.com/docs/en/cobol-zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# File control commands (READ, WRITE, REWRITE, STARTBR) and RESP handling
**Goal:** correct, handler-free command error checking.

```cobol
EXEC CICS READ FILE('CUSTFILE') INTO(CUST-REC)
    RIDFLD(WS-KEY) UPDATE RESP(WS-RESP) RESP2(WS-RESP2) END-EXEC
EVALUATE WS-RESP
    WHEN DFHRESP(NORMAL)   CONTINUE
    WHEN DFHRESP(NOTFND)   PERFORM NOT-FOUND
    WHEN OTHER             PERFORM CICS-ERROR
END-EVALUATE
EXEC CICS REWRITE FILE('CUSTFILE') FROM(CUST-REC) RESP(WS-RESP) END-EXEC
```
- `READ ... UPDATE` followed by REWRITE or UNLOCK; browse with STARTBR, READNEXT, ENDBR.
- Coding RESP on a command disables the default abend on error; always check it.
- `HANDLE CONDITION` and `HANDLE ABEND` are legacy and make flow hard to follow; avoid in new code.
- Resource names (FILE, MAPSET, TRANSID) must be defined in the CICS region (CEDA/CSD or bundle).

## Gotchas
- RESP is a binary fullword (`PIC S9(8) COMP`).
- READ UPDATE locks the record until the task syncpoints; keep the interval short.

## Self-check
READ a nonexistent key and verify NOTFND is handled without an abend (ASRA/AEIx).
