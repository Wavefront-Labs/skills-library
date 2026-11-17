---
id: computing-software.software-engineering.ada.gnatbind-elaboration-order
name: gnatbind-elaboration-order
category: computing-software
field: software-engineering
product: ada
tags: [ada, gnatbind-elaboration-order]
level: advanced
status: docs-checked
description: "Understand gnatbind and gnatlink phases, elaboration order inspection (-l -e -p), pragma Elaborate_All, Preelaborate."
sources:
  - https://docs.adacore.com/gnat_ugn-docs/html/gnat_ugn/gnat_ugn/building_executable_programs_with_gnat.html
  - https://docs.adacore.com/gnat_ugn-docs/html/gnat_ugn/gnat_ugn/elaboration_order_handling_in_gnat.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binder, elaboration order and linking
```
gnatbind main.ali         # bind: choose elaboration order, generate binder file
gnatbind -l main.ali      # output the chosen elaboration order
gnatbind -e main.ali      # output complete list of elaboration-order dependencies
gnatbind -p main.ali      # pessimistic (worst-case) order, for debugging
gnatlink main.ali
```
- Usage is `gnatbind [switches] mainprog[.ali]`; linking is done by `gnatlink`.
- Binder `-E` is not a dynamic-check switch: it stores tracebacks in exception occurrences (same as `-Ea`; `-Es` gives symbolic tracebacks). The dynamic model is the compiler switch `-gnatE`.
- `-p` only applies to the pre-20.x legacy elaboration models and is not for production use; it makes sense mainly with `-gnatE`.
- `-felab-order` forces the order from a file.
- Pure and Preelaborate units avoid elaboration order issues; the guide advises marking units `Pure` or `Preelaborate`, else `Elaborate_Body`.
- `pragma Elaborate_Body`; `pragma Elaborate_All (Other)` in a client unit's context clause.
- On an elaboration circularity the binder reports an error and tactics; the guide lists several ways to resolve it.

## Gotchas
- A failed elaboration check raises `Program_Error` at run time.

## Self-check
Build a two-package cycle with initialisation, observe the binder message.

## Checked
Method: docs-checked 2026-11-09 against the GNAT User's Guide pages Building Executable Programs with GNAT (gnatbind usage and switch list) and Elaboration Order Handling in GNAT. Dropped the old claim that `gnatbind -E` means dynamic elaboration check (it stores tracebacks) and the unsupported ada-auth.org source.
