---
id: computing-software.software-engineering.ada.jorvik-profile
name: jorvik-profile
category: computing-software
field: software-engineering
product: ada
tags: [ada, jorvik-profile]
level: sme
status: draft
description: "Ada 2022 Jorvik: Ravenscar relaxed to allow multiple entries per protected object and richer barriers."
sources:
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Jorvik profile
```ada
pragma Profile (Jorvik);
```
- Adds over Ravenscar: multiple entry queues per protected object, barriers not limited to one Boolean variable, entry-call timeouts remain disallowed (confirm in ARM D.13).
- Still no task rendezvous or abort; still static tasks.
- GNAT support level depends on compiler version (unconfirmed per release).
## Gotchas
- Jorvik code is not Ravenscar-compatible; keep Ravenscar if portability to older runtimes matters.
## Self-check
Compile a protected object with two entries under both profiles and compare.
