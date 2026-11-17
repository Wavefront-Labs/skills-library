---
id: computing-software.software-engineering.cobol.user-defined-functions
name: user-defined-functions
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, user-defined-functions, cobol-modern-features, function-id, user-defined-function, repository-paragraph]
level: advanced
status: docs-checked
description: "Write and call user-defined functions with FUNCTION-ID and REPOSITORY in Enterprise COBOL for z/OS 6.4."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FUNCTION-ID and user-defined functions
**Goal:** reusable value-returning functions. Rules below are from the Enterprise COBOL for z/OS 6.4 Language Reference.

```cobol
IDENTIFICATION DIVISION.
FUNCTION-ID. TAXED.
DATA DIVISION.
LINKAGE SECTION.
01 L-AMT  PIC S9(7)V99.
01 L-RES  PIC S9(7)V99.
PROCEDURE DIVISION USING L-AMT RETURNING L-RES.
    COMPUTE L-RES = L-AMT * 1.2
    GOBACK.
END FUNCTION TAXED.
```
Caller: name the function in the `REPOSITORY` paragraph (`REPOSITORY. FUNCTION TAXED.`), then `COMPUTE X = FUNCTION TAXED(Y)`.
- User-defined functions are part of the 2002 COBOL Standard. The FUNCTION-ID paragraph is required and must be the first paragraph of the IDENTIFICATION DIVISION.
- The function name is up to 30 characters; letters, digits, hyphen and underscore only; at least one letter; no leading or trailing hyphen. `FUNCTION-ID. name AS 'literal'` sets the externalised name.
- `ENTRY-INTERFACE` defaults to STATIC; `ENTRY-NAME` (COMPAT, LONGUPPER, LONGMIXED) overrides the PGMNAME option. LONGMIXED is not allowed when no AS literal is given.
- Once named in REPOSITORY, the function may be referenced without the keyword FUNCTION (unless specific rules require it). The name may not be LENGTH, RANDOM, SIGN, SUM or WHEN-COMPILED.
- Arguments are BY REFERENCE by default (the function sees the caller's data item); to pass effectively BY CONTENT use the CONTENT-OF intrinsic function, or declare BY VALUE on the function so it gets a temporary copy.
- The RETURNING item is output-only: its initial value is undefined, so set it before reading it.

## Gotchas
- Because the default is BY REFERENCE, assigning to a USING parameter changes the caller's data unless BY VALUE or CONTENT-OF is used.
- A function prototype definition has only the header (no declaratives, sections, paragraphs or statements).

## Self-check
`FUNCTION TAXED(100)` returns 120.00.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed in the 6.4 Language Reference text: FUNCTION-ID rules, REPOSITORY rules, BY REFERENCE/BY VALUE/CONTENT-OF for functions, 2002 Standard note. Removed: the claim that parameters are by content (wrong; default is BY REFERENCE), the RECURSIVE gotcha (no such clause on FUNCTION-ID), and version and GnuCOBOL support claims.
