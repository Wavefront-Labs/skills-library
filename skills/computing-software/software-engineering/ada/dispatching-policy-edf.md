---
id: computing-software.software-engineering.ada.dispatching-policy-edf
name: dispatching-policy-edf
category: computing-software
field: software-engineering
product: ada
tags: [ada, dispatching-policy-edf]
level: sme
status: draft
description: "Select with pragma Task_Dispatching_Policy: FIFO_Within_Priorities, Round_Robin_Within_Priorities, EDF_Across_Priorities."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dispatching policies and Round_Robin/EDF
```ada
pragma Task_Dispatching_Policy (FIFO_Within_Priorities);
```
- Other policies: `Round_Robin_Within_Priorities`, `Non_Preemptive_FIFO_Within_Priorities`, `EDF_Across_Priorities` (ARM D.2).
- `Ada.Dispatching`, `Ada.Dispatching.EDF` for deadlines.
- Whether the target runtime implements them is runtime-specific (confirm in runtime docs).
## Gotchas
- Pragma applies to the whole partition.
## Self-check
Compile with a non-supported policy and read the GNAT diagnostic.
