---
id: computing-software.software-engineering.cobol.legacy-cobol-refactoring
name: legacy-cobol-refactoring
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, legacy-cobol-refactoring, cobol-modernization, legacy-code-analysis, refactoring-legacy, dead-code, characterization-tests]
level: advanced
status: draft
description: "Understand old COBOL and refactor it in small, test-backed steps."
sources:
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading and refactoring legacy COBOL safely
**Goal:** change legacy code without breaking behavior.

1. Build a characterization test: capture real input files and outputs from the current build (golden files) before touching anything.
2. Map the program: list paragraphs, PERFORM/GO TO graph, files, copybooks, called programs, and external effects (`cobc -Xref`, IBM XREF listing, or a static-analysis tool).
3. Remove dead code only when the cross-reference shows no references and tests still match.
4. Make small structure-only changes: add scope terminators, rename ambiguous fields via REPLACING, extract repeated code into paragraphs, replace ALTER with flags.
5. Re-run the golden test after every step; commit each step.
6. Wrap proven logic as a callable subprogram or service rather than rewriting it in another language; rewrite only with parallel-run comparison.
- Wrapping as an API or REST service is available through products (for example IBM z/OS Connect, CICS web services); capabilities depend on version (unconfirmed).

## Gotchas
- Business rules often hide in odd PIC clauses and MOVE truncation; characterization tests expose them.
- Do not reformat and refactor in the same commit.

## Self-check
Run the golden test before and after each refactoring commit; all outputs byte-identical.
