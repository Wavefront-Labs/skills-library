---
id: computing-software.software-engineering.fortran.fixed-form-source
name: fixed-form-source
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, fixed-form-source, fortran-source-form]
level: practitioner
status: draft
description: "Read and maintain legacy fixed-form Fortran: columns 1-5 labels, column 6 continuation, 7-72 statements, C or star comments."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fixed-form source and its column rules
**Goal:** maintain old FORTRAN 77 style files without breaking the column rules.
- Fixed form (default for `.f`, `.for`, `.ftn`) uses columns: 1-5 statement label, 6 continuation mark (any non-blank, non-zero char), 7-72 statement text; text past column 72 is ignored.
- A `C`, `c` or `*` in column 1 (or `!` anywhere) starts a comment.
- Blanks are insignificant in fixed form: `DO 10 I = 1.5` parses as an assignment to variable `DO10I` (classic trap).
```fortran
C     FIXED FORM EXAMPLE
      PROGRAM OLD
      REAL X
      X = 1.0 +
     &    2.0
      PRINT *, X
      END
```
- gfortran: `-ffixed-form` forces fixed form, `-ffixed-line-length-none` or `-ffixed-line-length-132` relaxes column 72.
## Gotchas
- Code silently truncated at column 72 is the most common legacy bug; add `-ffixed-line-length-none` and rebuild to detect it.
- Do not mix tabs: gfortran accepts them as an extension only (`-Wtabs` warns).
## Self-check
Compile with `-Wall -ffixed-line-length-none` and diff behaviour against the default; any difference reveals truncated text.
