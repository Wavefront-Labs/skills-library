---
id: computing-software.software-engineering.nim.template-basics-untyped
name: template-basics-untyped
category: computing-software
field: software-engineering
product: nim
tags: [template-basics-untyped, templates, template, untyped, typed, substitution, lazy-evaluation, inline, nim]
level: practitioner
status: docs-checked
description: "Write templates for zero-overhead code substitution, using typed, untyped and varargs parameters and evaluation order."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Template basics and untyped parameters

Goal: use templates to abstract syntax without call overhead.

```nim
import std/times
template withTimer(body: untyped) =
  let t0 = cpuTime()
  body
  echo cpuTime() - t0
withTimer:
  heavyWork()
```
- A template is a simple form of macro: a substitution mechanism over the AST, processed in the semantic pass of the compiler. It is invoked like a procedure. `!=`, `>`, `>=`, `in`, `notin` and `isnot` are templates.
- The template "types" are the meta types `untyped`, `typed` and `typedesc`; a regular type implies a `typed` expression.
- `untyped`: no symbol lookup or type resolution before the expression is passed, so undeclared identifiers can be passed (`declareInt(x)`). `typed` fails for an undeclared identifier.
- Pass a block as the last argument with the colon syntax (`withFile(txt, "f.txt", fmWrite):` followed by the indented statements). The block parameter normally has to be `untyped`, because a `typed` body is type-checked first and cannot see procs the template declares (`undeclared identifier: p`).
- `varargs[untyped]` leaves even the number of arguments open, but a template cannot iterate over varargs, so it is mostly useful for macros.
- Templates are hygienic: local identifiers declared in a template cannot be accessed in the instantiation context, and most symbols bind from the definition scope. `mixin` and `bind` adjust binding as in generics.
- Build identifiers with backticks: `` `T name` `` becomes `Tmyint` for `name = myint`.
- `explicit immediate` templates are deprecated; a template whose parameters are all `untyped` is an immediate template.

Verify: `withTimer` prints elapsed time and `heavyWork` runs once.

## Checked

2026-11-08. Confirmed against the Nim Manual (doc/manual.md from the Nim repository), Templates chapter from the start through "Hygiene in templates" (read to that point; the later hygiene details, `inject` and `gensym` text were not read). Removed because not read there: "a parameter used twice is evaluated twice", "templates cannot be recursive" and the statement about return type options. tut1 and lib were not read and were dropped from sources.
Method: documentation only; no commands were run.
