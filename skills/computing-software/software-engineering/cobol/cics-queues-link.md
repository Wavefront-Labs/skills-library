---
id: computing-software.software-engineering.cobol.cics-queues-link
name: cics-queues-link
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, cics-queues-link, cobol-cics, cics-link, cics-xctl, ts-queue, td-queue]
level: advanced
status: draft
description: "Share data and call programs in CICS with TS and TD queues, LINK/XCTL and COMMAREA or channels."
sources:
  - https://www.ibm.com/docs/en/cics-ts
  - https://www.ibm.com/docs/en/cobol-zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Temporary storage, transient data, LINK and XCTL
**Goal:** inter-program communication inside CICS.

```cobol
EXEC CICS LINK PROGRAM('SUBPGM') COMMAREA(WS-COMM)
    LENGTH(LENGTH OF WS-COMM) RESP(WS-RESP) END-EXEC
EXEC CICS XCTL PROGRAM('NEXTPGM') COMMAREA(WS-COMM) END-EXEC
EXEC CICS WRITEQ TS QUEUE('MYQ') FROM(WS-ITEM) ITEM(WS-ITEM-NO) END-EXEC
EXEC CICS READQ TS QUEUE('MYQ') INTO(WS-ITEM) ITEM(1) END-EXEC
```
- `LINK` calls and returns; `XCTL` transfers control without return.
- TS queues (temporary storage) hold items by position and can be shared across tasks; TD queues (transient data) are read-once queues, often tied to batch or ICs.
- Channels and containers (`PUT CONTAINER`, `GET CONTAINER`) are the modern replacement for 32 KB-limited COMMAREAs.
- Do not use COBOL CALL to another CICS program unless it is a plain subroutine compiled without EXEC CICS (or share the same task through LE).

## Gotchas
- Unique queue names per user/terminal: build them with EIBTRMID.
- Clean up TS queues (DELETEQ) or they accumulate.

## Self-check
WRITEQ then READQ an item and verify the text round-trips.
