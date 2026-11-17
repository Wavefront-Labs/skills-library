---
id: computing-software.software-engineering.ada.gnatdoc-gnatmetric-gnatstub
name: gnatdoc-gnatmetric-gnatstub
category: computing-software
field: software-engineering
product: ada
tags: [ada, gnatdoc-gnatmetric-gnatstub]
level: practitioner
status: draft
description: "Generate docs and metrics: gnatdoc, gnatmetric complexity/LOC, gnatstub body skeletons from specs."
sources:
  - https://docs.adacore.com/gnat_ugn-docs/html/gnat_ugn/gnat_ugn.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# gnatdoc, gnatmetric and gnatstub
```
gnatdoc -P app.gpr                     # HTML docs from comments
gnatmetric -P app.gpr --complexity-cyclomatic --lines-all
gnatstub -P app.gpr src/pkg.ads        # create pkg.adb skeleton
```
- gnatmetric thresholds: `--syntax-all` and `--contract-all` options exist (see UG).
- gnatstub: `--force` overwrites existing body.
## Gotchas
- gnatstub bodies raise Program_Error until filled in.
## Self-check
Generate a stub for a spec and compile it.
