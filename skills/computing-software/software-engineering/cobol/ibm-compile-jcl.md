---
id: computing-software.software-engineering.cobol.ibm-compile-jcl
name: ibm-compile-jcl
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, ibm-compile-jcl, cobol-compiler-ibm, igywcl, compile-link-go, loadlib]
level: practitioner
status: draft
description: "Compile, link-edit and run an Enterprise COBOL program with JCL and the IBM-supplied procedure."
sources:
  - https://www.ibm.com/docs/en/cobol-zos
  - https://www.ibm.com/docs/en/zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compile-link-go JCL and cataloged procedures
**Goal:** get from source to load module on z/OS.

```jcl
//CLG   EXEC IGYWCLG,REGION=0M
//COBOL.SYSIN DD DSN=<USER>.COBOL.SRC(HELLO),DISP=SHR
//COBOL.SYSLIB DD DSN=<USER>.COPYLIB,DISP=SHR
//LKED.SYSLMOD DD DSN=<USER>.LOADLIB(HELLO),DISP=SHR
//GO.SYSOUT DD SYSOUT=*
```
- IBM supplies cataloged procs `IGYWC` (compile), `IGYWCL` (compile and link), `IGYWCLG` (compile, link, go) in the compiler's installation library; your site may rename them or provide wrappers (names per your installation; verify).
- Override a step's DD as `//stepname.ddname`; pass options with `PARM.COBOL='...'`.
- The load module is created in the data set named by `SYSLMOD`; run later with `EXEC PGM=HELLO` and a `STEPLIB` pointing at that library.

## Gotchas
- Missing `//COBOL.SYSLIB` makes COPY members unresolved (a clear message in SYSPRINT).
- Compile return code 4 is warnings, 8 or more is an error; the link step is skipped by COND on higher codes in the standard proc.

## Self-check
Submit the job, read RC=0000 for each step, then run the load module and see its output.
