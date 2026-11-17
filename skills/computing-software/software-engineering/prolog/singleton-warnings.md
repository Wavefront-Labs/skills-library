---
id: computing-software.software-engineering.prolog.singleton-warnings
name: singleton-warnings
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-warnings, singleton-warnings, style-check]
level: intro
status: draft
description: "Read and fix load-time warnings: singleton variables, discontiguous clauses, unused imports and style_check/1."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Load-time warnings
```
Warning: f.pl:3: Singleton variables: [X]
Warning: Clauses of foo/1 are not together in the source-file
```
- Rename unused variables to `_` or `_Name`; a `_Name` used twice gives "Singleton-marked variable appears more than once".
- Group all clauses of a predicate; otherwise add `:- discontiguous foo/1.`.
- Control: `:- style_check(-singleton).` (avoid), `:- style_check(+var_branches).`
- Missing predicates: `list_undefined/0` (library(check)) lists calls to undefined predicates.
## Gotchas
- A singleton warning is often a typo: check variable spelling first.
- `check/0` runs a full set of static checks.
## Self-check
Run `?- list_undefined.` on a project and fix every entry.
