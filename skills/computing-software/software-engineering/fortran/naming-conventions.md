---
id: computing-software.software-engineering.fortran.naming-conventions
name: naming-conventions
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, naming-conventions, fortran-style]
level: intro
status: draft
description: "Follow readable naming: lowercase keywords, snake_case identifiers, module and file name alignment, short procedures with intents."
sources:
  - https://fortran-lang.org/learn/best_practices/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Naming and layout conventions
**Goal:** write consistent Fortran.
- Fortran is case-insensitive, so choose lowercase keywords and snake_case names consistently.
- File named after the module: `geometry.f90` contains `module geometry`.
- Use descriptive names (`n_cells`, `total_mass`); avoid single letters outside math code.
- Constants lowercase or uppercase by project rule; kinds named `dp`, `sp`, `wp`.
- Indent two to four spaces; keep lines under 100 characters (limit is 132).
- Always: `implicit none`, `intent`, explicit `private` default in modules.
- Fortran-lang's learn pages list recommended practices.
## Gotchas
- Names longer than 63 characters are illegal.
- Avoid names that shadow intrinsics (`sum`, `size`, `index`); it compiles but confuses readers.
## Self-check
Run fprettify or fortitude over the code and review remaining warnings.
