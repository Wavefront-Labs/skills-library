---
id: computing-software.software-engineering.ada.controlled-types-finalization
name: controlled-types-finalization
category: computing-software
field: software-engineering
product: ada
tags: [ada, controlled-types-finalization]
level: advanced
status: draft
description: "Ada.Finalization Controlled and Limited_Controlled: Initialize, Adjust, Finalize, RAII-style resource handling."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/advanced-ada/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Controlled types and finalization
```ada
with Ada.Finalization;
type Handle is new Ada.Finalization.Limited_Controlled with record F : File_Type; end record;
overriding procedure Finalize (H : in out Handle);   -- closes on scope exit
```
- `Controlled` has `Initialize`, `Adjust` (after assignment), `Finalize`.
- Finalize runs on normal exit, exception and abort-deferred.
## Gotchas
- Finalize must not propagate exceptions (becomes Program_Error).
- Not allowed in SPARK and some safety profiles.
## Self-check
Print a message in Finalize and leave scope via an exception.
