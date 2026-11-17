---
id: computing-software.software-engineering.ada.type-invariants-predicates
name: type-invariants-predicates
category: computing-software
field: software-engineering
product: ada
tags: [ada, type-invariants-predicates]
level: advanced
status: docs-checked
description: "Ada Type_Invariant on private types, Static_Predicate / Dynamic_Predicate on subtypes and their checks."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/advanced-ada/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type invariants and subtype predicates
```ada
subtype Even is Integer with Dynamic_Predicate => Even mod 2 = 0;
subtype Vowel is Character with Static_Predicate => Vowel in 'a'|'e'|'i'|'o'|'u';
type Acct is private with Type_Invariant => Balance (Acct) >= 0;
```
- A static predicate can describe a non-contiguous set of values, and such a subtype can be used as a loop range: `for I in Test_Days loop`.
- Predicates are checked on all `in` and `out` parameters and on assignments and explicit initializations.
- Type invariants are checked on `out` parameters returned from subprograms declared in the same public scope, and on all initializations.
- Checks need `-gnata` (assertions are off by default).
## Gotchas
- Use a type invariant for private types, a predicate for visible subtypes.
## Self-check
Assign 3 to an Even variable (via a variable) and confirm the check fails with -gnata.

## Checked
2026-11-03. Confirmed in Introduction to Ada, Contract-Based Programming: `Static_Predicate`, `Dynamic_Predicate`, `Type_Invariant`, the check-location table, loop over a static-predicate subtype, `-gnata`. Corrected the old gotcha (the page says predicates are checked on in and out parameters). Removed the `case` use and the exception name (not on the pages read).
Method: documentation only; no commands were run.
