---
id: computing-software.software-engineering.ada.ghost-code
name: ghost-code
category: computing-software
field: software-engineering
product: ada
tags: [ada, ghost-code, spark-ghost-lemma]
level: advanced
status: docs-checked
description: "SPARK Ghost aspect on variables, functions, procedures and types: specification-only helpers that cannot affect program behaviour."
sources:
  - https://docs.adacore.com/spark2014-docs/html/lrm/
  - https://learn.adacore.com/courses/intro-to-spark/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ghost entities
```ada
function Is_Sorted (A : Arr) return Boolean is (for all I in A'First .. A'Last - 1 => A (I) <= A (I + 1)) with Ghost;
Old_Len : Natural := Len with Ghost;
```
- `Ghost` can annotate any entity: variables, types, subprograms and packages. GNATprove ensures a ghost entity cannot affect the program's behaviour.
- With assertions enabled, ghost code is executed like normal code so contracts that use it can run; you can also tell the compiler not to generate code for ghost entities.
- Ghost functions (e.g. `Get_Model`) expose information to contracts without exposing it to client code; ghost procedures operate on ghost variables or group intermediate assertions.
## Gotchas
- A ghost function is never used in production code.
## Self-check
Use a ghost predicate in a Post and prove a sort procedure.

## Checked
2026-11-03. Confirmed in Introduction to SPARK, chapter Proof of Functional Correctness (Ghost Code, Ghost Functions, Ghost Procedures, local and global ghost variables). Removed the `Assertion_Policy (Ghost => Ignore)` spelling and the Ghost_Assertion policy (not on the pages read).
Method: documentation only; no commands were run.
