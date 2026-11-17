---
id: computing-software.software-engineering.nim.nim-style-and-linting-flags
name: nim-style-and-linting-flags
category: computing-software
field: software-engineering
product: nim
tags: [nim-style-and-linting-flags, formatting-and-linting, style-guide, stylecheck, naming-conventions, warnings, hints, nep1, lint, nim]
level: practitioner
status: docs-checked
description: "Follow Nim naming and style conventions and enforce them with --styleCheck and warning flags."
sources:
  - https://nim-lang.org/docs/nep1.html
  - https://nim-lang.org/docs/nimc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Style guide, styleCheck and warnings

Goal: write consistent, warning-free code.

- NEP 1 style: two spaces per block (tabs not allowed), types in `PascalCase`, other identifiers `camelCase` (constants may use PascalCase), non-pure enum values carry an identifying prefix and use camelCase, pure enums use PascalCase, acronyms are treated as words (`parseUrl`, not `parseURL`), exception types end in `Error` or `Defect`, standard modules are imported as `std/os` or `std/[os, sysrand]`.
- `--styleCheck:off|hint|error` produces hints or errors for identifiers that break the style guide; `--styleCheck:usages` only enforces consistent spellings of identifiers, not the style on declarations.
- `--warningAsError:X:on|off` turns a specific warning X into an error; `--hint:X:on|off` toggles one hint. Real names in the compiler include `UnusedImport`, `Deprecated`, `ImplicitDefaultValue` (warnings) and `XDeclaredButNotUsed` (hint).
- `--panics:on|off` turns panics into process terminations (default off). `strictFuncs` and `strictNotNil` are enabled with `{.experimental: "strictFuncs".}` or `--experimental:strictFuncs` (see the experimental manual).

Gotchas:
- Scope warnings-as-errors to specific names rather than all warnings.

Verify: CI fails on an inconsistent name spelling.

## Checked

2026-11-02. Confirmed against nep1.md (indentation, casing, enums, acronyms, Error/Defect suffix, `std/` imports), advopt.txt (`--styleCheck`, `--warningAsError`, `--hint`, `--panics`), compiler/lineinfos.nim (warning and hint names) and manual_experimental.md (`strictFuncs`, `strictNotNil`). Removed: module-name, leading-underscore and Hungarian claims, `strictDefs`, the compiler-upgrade and declared-names gotchas.
Method: documentation only; no commands were run.
