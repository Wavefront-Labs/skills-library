---
id: computing-software.software-engineering.ada.gnat-compile-switches
name: gnat-compile-switches
category: computing-software
field: software-engineering
product: ada
tags: [ada, gnat-compile-switches, gnat-compiler]
level: practitioner
status: docs-checked
description: "Compile Ada with GNAT: -gnat2012/-gnat2022, -O, -g, -gnata, -gnatwa, -gnatyg, -fstack-check and common build modes."
sources:
  - https://docs.adacore.com/gnat_ugn-docs/html/gnat_ugn/gnat_ugn.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gnatmake/gcc switches and warnings
```
gcc -c -gnat2022 -gnata -gnatwa -gnatyg -g -O2 main.adb
gnatmake -gnat2022 main.adb -largs -static
```
- `-gnatwa` common warnings; `-gnatwe` warnings as errors; `-gnaty` style.
- Overflow checking is enabled by default (strict mode); `-gnato0` suppresses it and `-gnato??` selects the overflow mode; `-gnatp` suppresses all checks.
- `-gnatc` syntax and semantics only; `-gnatE` dynamic elaboration checks.
## Gotchas
- For projects with more than one directory, GNAT UG recommends a project file and gprbuild, which works similarly to gnatmake.
## Self-check
Compile a deliberate unused variable with and without -gnatwa.

## Checked
2026-11-03. Confirmed in the GNAT User's Guide (Building Executable Programs with GNAT): `-gnat2022`, `-gnata`, `-gnatwa`, `-gnatwe`, `-gnaty`/`-gnatyg`, `-gnatc`, `-gnatE`, `-gnatp`, `-fstack-check`, `-largs`, `-gnato` default. Replaced the unsupported "gnatmake is legacy" with the page's gprbuild recommendation.
Method: documentation only; no commands were run.
