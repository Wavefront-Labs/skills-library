---
id: computing-software.software-engineering.cobol.cics-pseudo-conversational
name: cics-pseudo-conversational
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, cics-pseudo-conversational, cobol-cics, pseudo-conversational, bms-map, send-map, receive-map]
level: advanced
status: draft
description: "Design pseudo-conversational CICS transactions with SEND MAP, RECEIVE MAP and RETURN TRANSID COMMAREA."
sources:
  - https://www.ibm.com/docs/en/cics-ts
  - https://www.ibm.com/docs/en/cobol-zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pseudo-conversational design and BMS screen interaction
**Goal:** screens without holding a task during user think time.

```cobol
IF EIBCALEN = 0
    EXEC CICS SEND MAP('CUSTM1') MAPSET('CUSTMS') ERASE END-EXEC
ELSE
    EXEC CICS RECEIVE MAP('CUSTM1') MAPSET('CUSTMS')
        INTO(CUSTM1I) RESP(WS-RESP) END-EXEC
    ...
END-IF
EXEC CICS RETURN TRANSID('CUST')
    COMMAREA(WS-COMM) LENGTH(LENGTH OF WS-COMM) END-EXEC
```
- A BMS mapset (assembler macros DFHMSD/DFHMDI/DFHMDF) generates a symbolic map copybook with fields `...I` (input) and `...O` (output), with attribute and length fields (`L`, `A`, `F`).
- The task ends at RETURN; CICS restarts the transaction when the user presses an AID key, and passes the COMMAREA.
- Inspect `EIBAID` and compare to `DFHENTER`, `DFHPF3`, `DFHCLEAR` from `DFHAID`.
- Map I/O errors: MAPFAIL when the user sent no data.

## Gotchas
- Keep state in COMMAREA (or TS queue/channel) not WORKING-STORAGE, which disappears at RETURN.
- Test field lengths for the `LOW-VALUES`/ `L = 0` condition before using input.

## Self-check
Run two exchanges of a screen and verify state survives through the COMMAREA.
