---
id: computing-software.software-engineering.ada.elaboration-order-checks
name: elaboration-order-checks
category: computing-software
field: software-engineering
product: ada
tags: [ada, elaboration-order-checks]
level: sme
status: docs-checked
description: "GNAT static elaboration model vs dynamic model, -gnatE, -gnatel diagnostics, and fixing Program_Error from elaboration."
sources:
  - https://docs.adacore.com/gnat_ugn-docs/html/gnat_ugn/gnat_ugn/elaboration_order_handling_in_gnat.html
  - https://docs.adacore.com/gnat_ugn-docs/html/gnat_ugn/gnat_ugn/building_executable_programs_with_gnat.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elaboration checks and static model
- The static model is the default model in GNAT. The dynamic model is enabled with the compiler switch `-gnatE`; it adds run-time checks, and an order obtained with it can still fail at run time.
- `-gnatel` prints informational messages about generated Elaborate and Elaborate_All pragmas. It only applies to the pre-20.x legacy elaboration models.
- Fix: `pragma Pure` or `Preelaborate` on the unit if possible, else `pragma Elaborate_Body`; in clients use `Elaborate` or `Elaborate_All` for the server unit.
- Binder switch `-p` picks a deliberately worst-case ("pessimistic") order (legacy models only, for debugging, not production). Binder `-f` forces an order from a file (written `-felab-order`).
- Circularities: the binder reports "Elaboration circularity detected" with suggested tactics; the guide lists tactics such as removing an Elaborate_All, using the dynamic model, or removing a dependency from the `-f` file.

## Gotchas
- Elaboration issues are build-order dependent; test a clean rebuild.

## Self-check
Create a call into a not-yet-elaborated package and capture the Program_Error.

## Checked
Method: docs-checked 2026-11-09 against the GNAT User's Guide pages Elaboration Order Handling in GNAT (switches, models, circularity section) and Building Executable Programs with GNAT (gnatbind switch list). Dropped the claim that the default model depends on GNAT version and the `-gnatd.G` flag, which neither page documents.
