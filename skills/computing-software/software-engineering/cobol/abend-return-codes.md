---
id: computing-software.software-engineering.cobol.abend-return-codes
name: abend-return-codes
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, abend-return-codes, cobol-exceptions, controlled-abend, ceedump, user-abend-code]
level: advanced
status: draft
description: "End programs deliberately on fatal errors with a message and a distinct code instead of dying at random."
sources:
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Controlled abends and return code policy
**Goal:** failures that operators and schedulers can interpret.

- Pattern: central `9999-ABEND` paragraph that DISPLAYs context (program, paragraph, key, status), sets RETURN-CODE and ends.
```cobol
9999-ABEND.
    DISPLAY 'ABEND IN ' WS-PROGRAM ' PARA ' WS-PARA ' STATUS ' WS-FS
    MOVE 16 TO RETURN-CODE
    GOBACK.
```
- On z/OS Language Environment a user abend can be raised with `CALL 'CEE3ABD' USING ABEND-CODE TIMING` (callable service; arguments per the LE Programming Reference; verify), which gives a dump.
- GnuCOBOL: `STOP RUN WITH ERROR STATUS 8` is accepted in newer versions (unconfirmed for older releases); or MOVE to RETURN-CODE.
- Log enough to restart: last key processed and counts.

## Gotchas
- Silent GOBACK with RETURN-CODE 0 after an error hides failures from the scheduler.
- Dumps contain data; follow site policy for retention.

## Self-check
Force a bad file status and confirm the job ends non-zero with the message in the log.
