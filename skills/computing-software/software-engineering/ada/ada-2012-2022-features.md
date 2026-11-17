---
id: computing-software.software-engineering.ada.ada-2012-2022-features
name: ada-2012-2022-features
category: computing-software
field: software-engineering
product: ada
tags: [ada, ada-2012-2022-features, ada-versions]
level: practitioner
status: draft
description: "Key additions: 2012 contracts, expression functions, iterators; 2022 delta aggregates, @, parallel loops, declare expressions."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ada 2012 and Ada 2022 features
- 2012: Pre/Post, Type_Invariant, predicates, `if`/`case`/quantified expressions, expression functions, `for ... of`, containers, multicore-friendly Ada.Locales.
- 2022: `'Image` on any object, delta aggregates `(R with delta ...)`, `@` target name, `declare` expressions, `[ ]` container aggregates, `Ada.Containers` bounded variants, parallel `for` blocks.
- `A := @ + 1;` is `A := A + 1;` (target name).
- Select with `-gnat2012` / `-gnat2022`; features land in GNAT in stages (confirm per version).
## Gotchas
- Ada 2022 containers [ ] aggregates need `Aggregate` aspect on the type.
## Self-check
Rewrite a loop with `@` and a declare expression and compile with -gnat2022.
