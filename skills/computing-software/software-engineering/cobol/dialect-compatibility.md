---
id: computing-software.software-engineering.cobol.dialect-compatibility
name: dialect-compatibility
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, dialect-compatibility, cobol-standards, cobol-85, cobol-2002, cobol-2014, dialect-config]
level: advanced
status: draft
description: "Port code between compilers by recognizing dialect differences and using strict standard modes."
sources:
  - https://www.iso.org/
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# COBOL 85, 2002, 2014 and vendor dialect differences
**Goal:** portable source.

- Milestones: COBOL-74, COBOL-85 (scope terminators, EVALUATE, INITIALIZE), 1989 intrinsic functions amendment, COBOL 2002 (OO, free format, TYPEDEF, user functions, national), COBOL 2014 (dynamic tables, pointer/bit enhancements, more intrinsics), later revisions (ISO/IEC 1989:2023, details unconfirmed).
- Vendor extensions: IBM (COMP-5 behavior, JSON/XML, OPTIONS), Micro Focus, GnuCOBOL (`-std=` presets), Fujitsu, ACUCOBOL.
- GnuCOBOL: `cobc -std=cobol2014 -Wall` warns on extensions; `-std=ibm` mimics IBM reserved words and behavior to ease porting.
- Keep a portability list for the shop: file ASSIGN conventions, DISPLAY behavior, collating sequence, SORT parameters, and dialect-only features.

## Gotchas
- Standard conformance is partial in all compilers.
- Results involving binary truncation, rounding mode, and file status 9x vary.

## Self-check
Compile the program with the strictest standard mode and treat every extension warning as a porting task.
