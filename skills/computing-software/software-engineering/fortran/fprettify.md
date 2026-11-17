---
id: computing-software.software-engineering.fortran.fprettify
name: fprettify
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, fprettify, fortran-tooling]
level: practitioner
status: draft
description: "Format free-form Fortran with fprettify, set indentation, and enforce it in CI."
sources:
  - https://github.com/fortran-lang/fprettify
  - https://github.com/PlasmaFAIR/fortitude
  - https://github.com/fortran-lang/fortls
  - https://forddocs.readthedocs.io/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# fprettify formatter
**Goal:** automate formatting.
```bash
pip install fprettify
fprettify --indent 2 --line-length 100 -r src/ app/
fprettify --diff src/m.f90        # show changes
fprettify --silent --diff -r src/ # CI: nonzero if changes needed (check flags)
```
- Config in `.fprettify.rc` (command-line options as lines).
- Works on free-form source only.
- Normalises whitespace, indentation, case of keywords (`--case`), and relation operators.
## Gotchas
- Not all constructs are formatted (preprocessor lines, complex continuation).
- Check CI behaviour on your version; exit codes for `--diff` have varied.
## Self-check
Run it twice; the second run changes nothing.
