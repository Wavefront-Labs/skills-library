---
id: computing-software.software-engineering.cobol.free-format-modern-syntax
name: free-format-modern-syntax
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, free-format-modern-syntax, cobol-modern-features, exit-perform, inline-comment, modern-syntax]
level: practitioner
status: docs-checked
description: "Use modern readable constructs where the compiler supports them: EXIT PERFORM, EXIT PARAGRAPH, scope terminators, and comment forms."
sources:
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
  - https://gnucobol.sourceforge.io/doc/gnucobol.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Newer syntax in GnuCOBOL: inline comments, EXIT PERFORM, END- terminators
**Goal:** more readable code on current compilers.
```cobol
PERFORM VARYING I FROM 1 BY 1 UNTIL I > N
    IF TBL(I) = KEY-VAL
        EXIT PERFORM
    END-IF
END-PERFORM
```
- `EXIT PERFORM` ends an in-line PERFORM and continues after `END-PERFORM`; `EXIT PERFORM CYCLE` ends only the current iteration. Both are meant for in-line PERFORM.
- `EXIT PARAGRAPH` and `EXIT SECTION` leave the current paragraph or section; `EXIT PROGRAM` and `EXIT FUNCTION` leave a program or user-defined function (EXIT PROGRAM is not legal in a function).
- `*>` starts a comment: as the first non-blank text for a full-line comment, or after statement text for a partial-line comment (column 7 or later in fixed format, any column in free).
- `ALLOCATE` and `FREE` manage BASED storage dynamically.
- `>>IF`, `>>ELSE`, `>>END-IF` and `>>DEFINE` are compiler-directing facilities that include or skip source.
- Use `-std=` to restrict features to a dialect when you need portability.

## Gotchas
- Using BASED storage before `ALLOCATE` or after `FREE` gives unpredictable results (usually an abort).

## Self-check
Compile the snippet with `cobc -x -free`.

## Checked
2026-11-02. Checked against the GnuCOBOL Programmer's Guide (EXIT, ALLOCATE, comments, compiler-directing facility, source formats). Removed: IBM compiler references, FUNCTION without the keyword via REPOSITORY, TYPEDEF and CONSTANT claims, and the minimum release advice.

Method: documentation only; no commands were run.
