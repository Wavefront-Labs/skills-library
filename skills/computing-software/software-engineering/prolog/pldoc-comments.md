---
id: computing-software.software-engineering.prolog.pldoc-comments
name: pldoc-comments
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-pldoc, pldoc-comments, mode-declaration]
level: practitioner
status: draft
description: "Document predicates with %! mode comments, +/-/? argument modes, @param tags and doc_server/1."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PlDoc
```prolog
%!  area(+Shape, -Area) is det.
%
%   Area of Shape.
%   @arg Shape  circle(R) or rect(W,H)
%   @error type_error(Shape, Term)
area(circle(R), A) :- A is pi * R ** 2.
```
- Modes: `+` input, `-` output, `?` either, `:` goal/closure, `@` unchanged, `!` mutable. Determinism: `det`, `semidet`, `nondet`, `multi`, `failure`.
- Run: `?- doc_server(4000).` and browse; `doc_save/2` writes static HTML.
## Gotchas
- Comments must start `%!` or `/** ... */` directly before the clause.
- Mode declarations are documentation only (not enforced).
## Self-check
Document a module and view it at `http://localhost:4000/`.
