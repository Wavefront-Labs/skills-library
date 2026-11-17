---
id: computing-software.software-engineering.cobol.return-code-special-register
name: return-code-special-register
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, return-code-special-register, cobol-subprograms, return-code, step-condition-code, exit-status]
level: practitioner
status: docs-checked
description: "Set and read RETURN-CODE to pass a code to a calling program or the operating system when a COBOL program ends."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RETURN-CODE and condition codes between programs
**Goal:** a consistent return-code protocol (Enterprise COBOL for z/OS rules).

```cobol
CALL 'VALIDATE' USING WS-REC
IF RETURN-CODE NOT = 0
    PERFORM REJECT
END-IF
...
MOVE 8 TO RETURN-CODE
GOBACK.
```
- RETURN-CODE is a special register with the implicit definition `01 RETURN-CODE GLOBAL PICTURE S9(4) USAGE BINARY VALUE ZERO`. In nested programs it is implicitly GLOBAL in the outermost program. Set it with `MOVE 8 TO RETURN-CODE` or `COMPUTE RETURN-CODE = 8`.
- When a program ends and control returns to a calling COBOL program, the caller's RETURN-CODE is set to the called program's RETURN-CODE value. When control returns to the operating system, the value is passed as the user return code; the operating system decides which values are supported, which may be fewer than the register can hold.
- `STOP RUN` ends the run unit using RETURN-CODE modulo 4096 as the return code.
- RETURN-CODE does not carry a value back from an invoked method or from `CALL ... RETURNING`, and it does not return information from a Language Environment callable service.
- You can use RETURN-CODE in a function wherever an integer argument is allowed.

## Gotchas
- Because the called program's value overwrites the caller's, a callee that never sets it returns whatever it last held. Save your own RETURN-CODE in a working-storage item before a CALL if you still need it, and set the register explicitly before GOBACK.
- Choose the numbers your site's job scheduler checks; this source does not define any convention such as 0/4/8/12/16.

## Self-check
Run the program as a job step or from a shell and compare the reported step condition code or exit status to the value you set; for values over 4095 expect the modulo-4096 effect on STOP RUN.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted): the RETURN-CODE special register section and the STOP statement (modulo 4096). Removed the 0/4/8/12/16 JCL COND convention, the GnuCOBOL process-exit-status 0-255 claim and the Unix mod 256 wrap claim, because none appear in the source. Removed the unread ISO, ibm.com/docs and GnuCOBOL sources.
Method: documentation only; no commands were run.
