---
id: computing-software.software-engineering.ada.protected-barriers-requeue
name: protected-barriers-requeue
category: computing-software
field: software-engineering
product: ada
tags: [ada, protected-barriers-requeue]
level: advanced
status: draft
description: "Protected entry barrier semantics, entry families, requeue, and Ravenscar-safe single-entry patterns."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/advanced-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Barriers, entry bodies and requeue
```ada
entry Get (X : out Item) when Full is begin X := Buf; Full := False; end Get;
```
- Barriers depend on protected state only (not entry parameters); keep them simple.
- `requeue Other;` from an entry body.
- Ravenscar allows at most one entry per protected object with a simple Boolean barrier.
## Gotchas
- Calling an entry of the same object from inside it is a bounded error.
## Self-check
Write a one-slot buffer with Put/Get entries and test with producer/consumer tasks.
