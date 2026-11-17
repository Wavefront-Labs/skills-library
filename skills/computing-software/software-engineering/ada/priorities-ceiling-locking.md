---
id: computing-software.software-engineering.ada.priorities-ceiling-locking
name: priorities-ceiling-locking
category: computing-software
field: software-engineering
product: ada
tags: [ada, priorities-ceiling-locking, ada-priority-scheduling]
level: advanced
status: draft
description: "Ada Priority aspect, System.Priority range, Priority_Ceiling, Ceiling_Locking and priority inversion avoidance."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Task priorities and ceiling locking
```ada
task T with Priority => System.Priority'First + 2;
protected P with Priority => System.Priority'Last is ... end P;
pragma Locking_Policy (Ceiling_Locking);
```
- The ceiling must be at least the highest priority of any caller; violating it raises `Program_Error`.
- `System.Priority` and `System.Interrupt_Priority` ranges are target-defined.
## Gotchas
- `Ceiling_Locking` is not on by default in all GNAT runtimes; set the pragma explicitly.
## Self-check
Call a protected procedure from a higher-priority task than the ceiling and see Program_Error.
