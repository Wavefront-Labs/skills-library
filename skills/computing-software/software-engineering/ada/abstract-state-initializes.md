---
id: computing-software.software-engineering.ada.abstract-state-initializes
name: abstract-state-initializes
category: computing-software
field: software-engineering
product: ada
tags: [ada, abstract-state-initializes]
level: advanced
status: docs-checked
description: "Hide package state in SPARK with Abstract_State, Initializes, Refined_State and Refined_Global."
sources:
  - https://docs.adacore.com/spark2014-docs/html/lrm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Abstract_State, Initializes and Refined_State
```ada
package Log with Abstract_State => (State), Initializes => State is ... end Log;
package body Log with Refined_State => (State => (Buf, Len)) is ...
```
- Abstract_State options include `Ghost`, `Synchronous`, `External` (with `Async_Readers`, `Async_Writers`, `Effective_Reads`, `Effective_Writes`) and `Part_Of => abstract_state`, which lets another package's state be a constituent of this abstraction.
- `Refined_Global`/`Refined_Depends` repeat the contracts in terms of concrete state.
- A package with a body that declares abstract state must complete it with `Refined_State`.
- `Initializes` may only appear on a package specification and may name only state abstractions or objects declared in the visible part.
## Gotchas
- Every entity of the hidden state must be a constituent of exactly one abstract state in `Refined_State`, and may not be listed twice.
## Self-check
Add a hidden variable without Refined_State coverage and read the error.

## Checked
2026-11-03. Confirmed in the SPARK Reference Manual, Packages (7.1 Abstraction of State, Abstract_State options grammar, Initializes, Refined_State rules). Corrected `External_Name` (the Abstract_State option is `External`).
Method: documentation only; no commands were run.
