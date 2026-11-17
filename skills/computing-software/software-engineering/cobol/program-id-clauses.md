---
id: computing-software.software-engineering.cobol.program-id-clauses
name: program-id-clauses
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, program-id-clauses, cobol-structure, initial-program, recursive-program, nested-program, end-program]
level: practitioner
status: docs-checked
description: "Declare programs with PROGRAM-ID attributes (INITIAL, COMMON, RECURSIVE) and nest or batch several programs in one source file."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PROGRAM-ID, INITIAL, COMMON, RECURSIVE and nested programs
**Goal:** pick the right PROGRAM-ID attribute and close programs correctly (Enterprise COBOL for z/OS rules).

```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. OUTER.
...
    IDENTIFICATION DIVISION.
    PROGRAM-ID. INNER IS COMMON PROGRAM.
    ...
    END PROGRAM INNER.
END PROGRAM OUTER.
```
- PROGRAM-ID is required and must be the first paragraph of the IDENTIFICATION DIVISION. The program-name is a user-defined word or an alphanumeric literal (not a figurative constant). With PGMNAME(COMPAT) or LONGUPPER a user-defined word is up to 30 characters of letters, digits, hyphen and underscore, with at least one letter and no leading or trailing hyphen; as a literal LONGUPPER and LONGMIXED allow up to 160 characters. The PGMNAME option itself is described in the Programming Guide.
- `IS INITIAL PROGRAM`: each time the program is called, it and any programs nested in it are put in the initial state: WORKING-STORAGE is re-initialized (items with VALUE get the value, others are undefined), files with internal connectors are not open, PERFORM control mechanisms are reset and altered GO TOs revert. A program is also in initial state on its first call in a run unit and on the first call after a CANCEL naming it or a program that contains it. Not supported with the THREAD compiler option.
- `IS COMMON PROGRAM`: only for nested programs. The program can be called from its siblings and from programs contained in them, not just from its parent. Without COMMON, a directly nested program's name can be referenced only from its containing program.
- `IS RECURSIVE`: only on the outermost program of a compilation unit, and a recursive program cannot contain nested programs. It may be re-entered while an earlier invocation is active; without it, an active program cannot be re-entered. WORKING-STORAGE is static, initialized on the first entry and shared in last-used state by all invocations, so keep per-call state in LOCAL-STORAGE (allocated, initialized and freed per invocation). Not supported in a recursive program: ALTER, GO TO with no procedure-name, RERUN, SEGMENT-LIMIT and USE FOR DEBUGGING. RECURSIVE is required for programs compiled with THREAD, which also does not support nested programs.
- Contained programs can see a data item only if it is declared with GLOBAL (level 01 entries only) in a containing program, and they do not redefine the same name.
- `END PROGRAM name.` must match the PROGRAM-ID. Every program needs it except an outermost program that contains no nested programs and is not followed by another program in the same source (a batch compile).

## Gotchas
- Without INITIAL, WORKING-STORAGE keeps its values between CALLs after the first (a common source of "second call behaves differently" bugs). CANCEL puts the program back in the initial state.
- How a program is named in a load module or by the linker is outside this source; check your platform's binder or linker documentation.

## Self-check
Call a subprogram twice that increments a counter: without INITIAL it should print 1 then 2; with INITIAL it prints 1 then 1.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted): Chapter 15 PROGRAM-ID paragraph (program-name rules, RECURSIVE, COMMON, INITIAL), nested programs and conventions for program-names, End program markers, and the GLOBAL clause. Removed the claim that nested programs "share nothing by default" in favour of the documented GLOBAL rule, and the load-module naming statement for z/OS (link step, not read). Removed the unread ISO, ibm.com/docs and GnuCOBOL sources.
Method: documentation only; no commands were run.
