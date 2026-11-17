---
id: computing-software.software-engineering.ada.aarm-reading-the-arm
name: aarm-reading-the-arm
category: computing-software
field: software-engineering
product: ada
tags: [ada, aarm-reading-the-arm]
level: practitioner
status: draft
description: "Navigate the Ada Reference Manual: section numbering, annexes, legality vs static/dynamic semantics, AARM notes."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading the ARM and AARM
- Layout: 1 General, 2 Lexical, 3 Declarations/Types, 4 Names/Expressions, 5 Statements, 6 Subprograms, 7 Packages, 8 Visibility, 9 Tasks, 10 Structure, 11 Exceptions, 12 Generics, 13 Representation. Annexes A-K, plus L-Q indices.
- Each clause: Syntax, Name Resolution, Legality, Static Semantics, Dynamic Semantics, Implementation Requirements/Permissions/Advice.
- Annotated (AARM) adds rationale, "ramification" and "implementation note" text; web versions on ada-auth.org (see Ada 2012/2022 editions).
## Gotchas
- "Bounded error" and "erroneous execution" are distinct; compilers may detect, not required.
## Self-check
Locate the rule for 'Class conversion legality and quote its heading.
