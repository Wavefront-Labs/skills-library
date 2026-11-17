---
id: computing-software.software-engineering.prolog.doc-save
name: doc-save
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, doc-save, module-header-doc]
level: advanced
status: draft
description: "Write module header docs (`/** <module> ... */`), @tbd, @see tags, and export HTML with doc_save/2."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Module header documentation
```prolog
:- module(shapes, [area/2]).
/** <module> Geometry helpers

Shapes and areas.

@author Name
@license MIT
*/
?- doc_save(shapes, [doc_root(docs), recursive(true)]).
```
Markdown is supported in comments; `[[pred/N]]` creates links.
## Gotchas
- Without a `/** <module> */` header the module summary stays empty.
- `doc_save` requires loading `library(pldoc/doc_files)`.
## Self-check
Generate static HTML and open `docs/index.html`.
