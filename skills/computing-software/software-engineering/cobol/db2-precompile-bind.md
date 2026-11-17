---
id: computing-software.software-engineering.cobol.db2-precompile-bind
name: db2-precompile-bind
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, db2-precompile-bind, cobol-db2, dbrm, bind-package, sql-coprocessor, db2-precompiler]
level: advanced
status: draft
description: "Prepare an embedded-SQL COBOL program: compile with the SQL coprocessor (or precompile), bind a package, run with a plan."
sources:
  - https://www.ibm.com/docs/en/db2-for-zos
  - https://www.ibm.com/docs/en/cobol-zos
  - https://www.ibm.com/docs/en/zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Precompile or coprocessor, DBRM, BIND PACKAGE and PLAN
**Goal:** the build steps beyond a plain compile.

- Modern: compile with the DB2 coprocessor option `SQL` on the COBOL compiler (Enterprise COBOL V4+), which produces a DBRM and the object in one step. Legacy: run the separate DB2 precompiler (`DSNHPC`) first.
- `BIND PACKAGE(collection) MEMBER(prog) ...` then `BIND PLAN` including that collection (or use package lists), via `DSN` command processor or TSO batch (`IKJEFT01`).
```jcl
//RUN EXEC PGM=IKJEFT01
//SYSTSIN DD *
  DSN SYSTEM(DB2P)
  RUN PROGRAM(CUSTRPT) PLAN(CUSTPLAN) LIB('<USER>.LOADLIB')
  END
/*
```
- Authorization (BINDADD, EXECUTE) and isolation level (e.g. `ISOLATION(CS)`) are bind options; consult the DB2 SQL reference for current syntax.
- The DBRM and load module must come from the same compile, or you get SQLCODE -818 (timestamp mismatch).

## Gotchas
- Recompile and rebind after any SQL change; rebind alone does not fix source changes.
- SQL in copybooks is expanded at precompile; COPY order matters.

## Self-check
Run the program against the test subsystem and check the bind produced the expected access path (EXPLAIN).
