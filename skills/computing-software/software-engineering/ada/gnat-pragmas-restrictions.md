---
id: computing-software.software-engineering.ada.gnat-pragmas-restrictions
name: gnat-pragmas-restrictions
category: computing-software
field: software-engineering
product: ada
tags: [ada, gnat-pragmas-restrictions]
level: advanced
status: docs-checked
description: "Use gnat.adc / pragma Restrictions, Normalize_Scalars, Initialize_Scalars and gnatbind -r."
sources:
  - https://docs.adacore.com/gnat_ugn-docs/html/gnat_ugn/gnat_ugn.html
  - https://www.ada-auth.org/standards/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restrictions and configuration pragmas
```ada
pragma Restrictions (No_Exceptions, No_Allocators, No_Recursion);
pragma Normalize_Scalars;
pragma Initialize_Scalars;   -- GNAT: init with invalid values
pragma Suppress (Overflow_Check);
```
- Configuration pragmas go in `gnat.adc` or `Local_Configuration_Pragmas` in a gpr.
- `gnatbind -r` generates the list of pragma Restrictions that could be applied to the program (useful for audit); it does not list the ones in force.
- Extra configuration files can be passed with `gcc -gnatec=path`; `gnat.adc` is used when present (ignored with `-gnatA`).
- `-gnatr` treats Restrictions as Restriction_Warnings during development.
## Gotchas
- `Initialize_Scalars` gives uninitialized scalars invalid values; pair it with `-gnatV` validity checks.
## Self-check
Add No_Allocators and confirm a `new` is rejected.

## Checked
2026-11-03. Confirmed in the GNAT User's Guide: `gnat.adc`, `-gnatec=`, `-gnatA`, `gnatbind -r` meaning, Initialize_Scalars with validity checks, `pragma Restrictions` use. Corrected `gnatbind -r` (it suggests applicable restrictions). Removed the unconfirmed "enforced by binder" gotcha.
Method: documentation only; no commands were run.
