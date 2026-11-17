---
id: computing-software.software-engineering.ada.gnatformat-gnatpp-gnatcheck
name: gnatformat-gnatpp-gnatcheck
category: computing-software
field: software-engineering
product: ada
tags: [ada, gnatformat-gnatpp-gnatcheck, gnat-tools]
level: practitioner
status: draft
description: "Format Ada with gnatpp or gnatformat and enforce coding rules with gnatcheck and style switches."
sources:
  - https://docs.adacore.com/gnat_ugn-docs/html/gnat_ugn/gnat_ugn.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Formatting and static rule checking
```
gnatpp -P app.gpr -rnb src/*.adb            # pretty print, backup none
gnatcheck -P app.gpr -rules +RStyle_Checks +RGoto_Statements
gnatcheck -P app.gpr -rules -from=rules.txt
```
- Newer toolchains ship `gnatformat` (Alire crate) as formatter; confirm availability.
- Rules in a file: `+RRecursive_Subprograms`.
## Gotchas
- Run formatter before commit to avoid noisy diffs.
## Self-check
Run gnatcheck for Goto_Statements on a file containing goto.
