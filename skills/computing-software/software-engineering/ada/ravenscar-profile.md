---
id: computing-software.software-engineering.ada.ravenscar-profile
name: ravenscar-profile
category: computing-software
field: software-engineering
product: ada
tags: [ada, ravenscar-profile, ada-ravenscar]
level: advanced
status: draft
description: "Enable pragma Profile (Ravenscar): static tasks, protected objects, no rendezvous, deterministic scheduling for analysable systems."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/Ada_For_The_Embedded_C_Developer/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ravenscar profile restrictions
```ada
pragma Profile (Ravenscar);
pragma Task_Dispatching_Policy (FIFO_Within_Priorities);   -- implied
pragma Locking_Policy (Ceiling_Locking);                   -- implied
```
- Allowed: library-level tasks and protected objects, `delay until`, protected entries with one barrier.
- Forbidden: task entries, select, abort, dynamic priorities, task hierarchies, relative delay.
- Run on a runtime that supports it (e.g. embedded-runtimes `light-tasking`/`embedded`; names per target, unconfirmed).
## Gotchas
- Tasks must be declared at library level and have `Priority`.
## Self-check
Add a `select` statement and read the restriction violation.
