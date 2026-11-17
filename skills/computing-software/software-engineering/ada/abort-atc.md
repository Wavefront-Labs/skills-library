---
id: computing-software.software-engineering.ada.abort-atc
name: abort-atc
category: computing-software
field: software-engineering
product: ada
tags: [ada, abort-atc]
level: sme
status: draft
description: "Ada abort statement and select-then-abort (ATC): semantics, abort-deferred regions and why it is restricted in Ravenscar."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Abort and asynchronous transfer of control
```ada
select
   delay 2.0;      -- triggering alternative
then abort
   Long_Computation;
end select;
abort Worker;       -- terminates the task (and dependents)
```
- Abort takes effect at abort completion points; protected actions and finalisation are abort-deferred.
- Banned by `pragma Restrictions (No_Abort_Statements, No_Select_Statements)` / Ravenscar.
## Gotchas
- Aborting during an update of shared state can leave it inconsistent.
## Self-check
Abort a looping task and confirm `'Terminated` becomes true.
