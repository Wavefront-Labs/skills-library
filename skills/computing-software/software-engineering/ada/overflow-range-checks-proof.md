---
id: computing-software.software-engineering.ada.overflow-range-checks-proof
name: overflow-range-checks-proof
category: computing-software
field: software-engineering
product: ada
tags: [ada, overflow-range-checks-proof]
level: practitioner
status: draft
description: "Make SPARK prove absence of runtime errors: bounded subtypes, preconditions on inputs, intermediate widening."
sources:
  - https://docs.adacore.com/spark2014-docs/html/ug/
  - https://learn.adacore.com/courses/intro-to-spark/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Proving overflow, range and index checks
```ada
function Add (X, Y : Natural) return Natural with Pre => X <= 1000 and Y <= 1000;
subtype Small is Integer range 0 .. 1000;
```
- Use narrow subtypes for parameters; strengthen preconditions at the boundary.
- Cast to a larger type before arithmetic or use `Big_Integers` in ghost code.
- Counter-examples: `--counterexamples=on` where supported (confirm per version).
## Gotchas
- A postcondition that restates the body adds no value; state properties.
## Self-check
Prove an Add with narrowed ranges and confirm no unproved checks.
