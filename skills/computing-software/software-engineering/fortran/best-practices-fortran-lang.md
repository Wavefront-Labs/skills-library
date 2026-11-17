---
id: computing-software.software-engineering.fortran.best-practices-fortran-lang
name: best-practices-fortran-lang
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, best-practices-fortran-lang, fortran-style]
level: practitioner
status: draft
description: "Apply the Fortran-lang best practice guides: floating point, modules, performance, and interoperability guidance."
sources:
  - https://fortran-lang.org/learn/best_practices/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fortran-lang best practices
**Goal:** use community guidance.
- Fortran-lang publishes best-practice pages (floating point, modules, performance, API design, naming) at fortran-lang.org under Learn.
- Recurring advice: prefer modules over external procedures; kind constants; `intent` everywhere; `allocatable` over `pointer`; `private` by default; use `do concurrent` and array operations for parallelism-friendly code; avoid `common`.
- Pair with a linter: `fortitude` (PlasmaFAIR) checks many of these rules.
- Use a build tool (fpm or CMake) and tests from day one.
## Gotchas
- Guidance evolves; read the live pages rather than relying on memory.
- Some advice (such as always passing assumed-shape) has performance implications.
## Self-check
Run a representative module through the checklist and fix the findings.
