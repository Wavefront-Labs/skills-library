---
id: computing-software.software-engineering.cobol.stop-goback-exit
name: stop-goback-exit
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, stop-goback-exit, cobol-control-flow, stop-run, goback, exit-program, return-code]
level: practitioner
status: docs-checked
description: "Terminate a program correctly: STOP RUN ends the run unit; GOBACK and EXIT PROGRAM return to the caller."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STOP RUN, GOBACK, EXIT PROGRAM and RETURN-CODE
**Goal:** end programs without ending the caller by accident (Enterprise COBOL for z/OS 6.4 wording).

- `STOP RUN`: terminates execution and returns control to the system, using the current RETURN-CODE value modulo 4096 as the return code. It closes all files of all programs in the run unit and frees dynamic-length buffers. Statements after it in the same sentence do not run. From a subprogram it returns directly to the program that called the main program.
- `GOBACK`: acts like EXIT PROGRAM in a called program and like STOP RUN in a main program (returning to the calling program, which can be the system). In a called program with the INITIAL attribute it is equivalent to also doing a CANCEL of that program.
- `EXIT PROGRAM`: with a CALL active, returns to the statement after the CALL; with no CALL active, control passes on to the next executable statement. An INITIAL program also acts as if CANCELled. If a called program runs off its end, an implicit EXIT PROGRAM is executed.
- Format 1 `EXIT.` alone is treated as CONTINUE.
- `STOP literal` suspends the program for an operator; IBM prefers ACCEPT and DISPLAY, and says not to use it with THREAD.
- RETURN-CODE is a special register defined as `S9(4) BINARY VALUE ZERO` with GLOBAL. Set it with `MOVE 8 TO RETURN-CODE` or COMPUTE before leaving; when control returns to the operating system it is passed as a user return code (the OS decides which values are supported); when control returns to a COBOL caller, the caller's RETURN-CODE is set to the called program's.

## Gotchas
- GOBACK, EXIT PROGRAM and STOP RUN should be the last statement in a sentence, since following statements are not executed.
- Do not use GOBACK or EXIT PROGRAM in a declarative with the GLOBAL phrase.
- RETURN-CODE is not set by a CALL that uses RETURNING, or by INVOKE.

## Self-check
Check that every called program ends with GOBACK or EXIT PROGRAM, and that STOP RUN appears only where the whole run unit should end.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the STOP statement, GOBACK statement, EXIT statement (formats 1 and 2) and RETURN-CODE special register sections. Confirmed all claims above. Removed: "STOP RUN in a subprogram terminates the caller too" (IBM's table says it returns directly to the program that called the main program), "STOP RUN RETURNING n / GOBACK RETURNING n" (neither is in the 6.4 formats), "EXIT PROGRAM as a main program does nothing" (reworded to IBM's wording), "overwritten by every CALL return" (reworded), "prefer GOBACK everywhere", and the unread ISO, ibm.com/docs root and GnuCOBOL sources.
Method: documentation only; no commands were run.
