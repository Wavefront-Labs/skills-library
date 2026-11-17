---
id: computing-software.software-engineering.cobol.ibm-language-environment
name: ibm-language-environment
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, ibm-language-environment, cobol-compiler-ibm, language-environment, ceeopts, ceedump, le-runtime]
level: advanced
status: draft
description: "Tune and diagnose Enterprise COBOL programs with LE runtime options and the CEEDUMP report."
sources:
  - https://www.ibm.com/docs/en/cobol-zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Language Environment runtime options and diagnostics (CEEOPTS, CEEDUMP)
**Goal:** debug runtime failures on z/OS.

- Runtime options are set with `PARM='/ABTERMENC(ABEND)'` style, the `CEEOPTS` DD, `#pragma`-style CEEUOPT module, or installation defaults.
```jcl
//CEEOPTS DD *
 RPTOPTS(ON),RPTSTG(ON),TRAP(ON),ALL31(ON)
/*
//CEEDUMP DD SYSOUT=*
```
- `RPTOPTS(ON)` lists the options in effect at termination; `RPTSTG(ON)` reports storage use.
- `TRAP(ON)` lets LE handle program interrupts (producing a CEE messages and CEEDUMP) instead of a raw system abend; `ABTERMENC(ABEND)` makes unhandled conditions abend (with a user abend code) rather than return RC.
- A CEEDUMP shows the traceback with program names, statement/offset numbers (when compiled with OFFSET or TEST) and the failing condition (such as CEE3207S for a system or user abend).
- Common messages: IGZ0xxx (COBOL runtime), CEEnnnn (LE).

## Gotchas
- Options of the form PARM='/opts' need the slash because the part before it is passed to the program.
- Some options cannot be overridden if the installation sets them as non-overridable.

## Self-check
Add RPTOPTS(ON) to a test job and verify the options report prints at program end.
