---
id: computing-software.software-engineering.prolog.dynamic-declaration
name: dynamic-declaration
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, dynamic-declaration, discontiguous-multifile]
level: practitioner
status: docs-checked
description: "Declare predicates with dynamic/1, discontiguous/1, multifile/1 and table/1, and know what each prevents."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Predicate property declarations
```prolog
:- dynamic seen/1.
:- discontiguous rule/2.
:- multifile hook/1.
:- dynamic(user:prolog_file_type/2).
?- predicate_property(seen(_), dynamic).
```
- `dynamic` declares that the definition may change at runtime (assert/retract); in the multithreaded version the clauses are shared between threads (`thread_local/1` gives each thread its own).
- `discontiguous` tells the system the clauses of the predicate might not be together in the source file.
- `multifile` lets a predicate be defined over more than one file, so `consult/1` does not redefine it when a new definition is found.
## Gotchas
## Self-check
Write clauses for a predicate in two places in one file and check what the system reports with and without a `discontiguous` declaration.

## Checked

2026-11-02. SWI-Prolog manual declaration entries: dynamic/1 (assert/retract, shared between threads, thread_local/1 alternative), discontiguous/1 (style_check/1), multifile/1 (stops consult from redefining). Removed: the reload behaviour and the module-qualified hook gotcha (not read in the fetched sections).

Method: documentation only; no commands were run.
