---
id: computing-software.software-engineering.ada.interfaces-c-import-export
name: interfaces-c-import-export
category: computing-software
field: software-engineering
product: ada
tags: [ada, interfaces-c-import-export, ada-interfacing]
level: practitioner
status: docs-checked
description: "Call C from Ada and vice versa: Interfaces.C types, the Import and Export aspects, Convention C, External_Name and chars_ptr strings."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/Ada_For_The_Embedded_C_Developer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interfaces.C, Import and Export
```ada
with Interfaces.C; use Interfaces.C;
function C_Abs (X : int) return int with Import, Convention => C, External_Name => "abs";
procedure Cb (X : int) with Export, Convention => C, External_Name => "ada_cb";
```
- `Import => True` plus `Convention => C` binds a C function or variable; `External_Name` gives the C name; `Export => True` exposes an Ada subprogram or variable to C.
- `Interfaces.C.Strings.New_String` and `chars_ptr` carry C strings.
- `System.Address` stands in for a C struct pointer in generated bindings.
## Gotchas
- A C function you import is not checked by the Ada compiler; the Ada profile must match the C one.
## Self-check
Import a C function with `External_Name` and call it from a small Ada main.

## Checked
2026-11-03. Confirmed in Introduction to Ada, Interfacing with C: Import/Export aspects, `Convention => C`, `External_Name`, `New_String`, `chars_ptr`, `System.Address` in generated bindings. Removed `Value`, `Free`, `char_array`, the linker-switch line and the array-passing advice (not on the pages read). The `C_Abs`/`abs` example is illustrative.
Method: documentation only; no commands were run.
