---
id: computing-software.software-engineering.fortran.ford-docs
name: ford-docs
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, ford-docs, fortran-tooling]
level: practitioner
status: draft
description: "Generate API docs from Fortran comments with FORD using ! docstrings and a project file."
sources:
  - https://github.com/fortran-lang/fprettify
  - https://github.com/PlasmaFAIR/fortitude
  - https://github.com/fortran-lang/fortls
  - https://forddocs.readthedocs.io/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FORD documentation generator
**Goal:** publish API documentation.
```bash
pip install ford
ford project.md
```
`project.md` header:
```
---
project: MyProj
src_dir: ./src
output_dir: ./doc
author: Your Name
---
Project description in Markdown.
```
- Document entities with `!!` after or before declarations:
```fortran
real function area(r) !! Compute circle area
  real, intent(in) :: r !! radius
```
- Produces HTML with call graphs (requires Graphviz).
- Useful in CI to publish on GitHub Pages.
## Gotchas
- Docstring marker defaults (`!!`) and metadata keys can be configured; verify with the FORD docs for your version.
- Graphs need Graphviz installed.
## Self-check
Generate docs and confirm module and procedure pages appear with the docstrings.
