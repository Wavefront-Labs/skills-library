---
id: computing-software.software-engineering.prolog.module-declaration-export
name: module-declaration-export
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-modules, module-declaration-export, module-export]
level: practitioner
status: docs-checked
description: "Declare a module with module/2, export predicates and operators in the public list and call non-exported predicates qualified."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/man/module.plx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module declaration
```prolog
:- module(shapes, [area/2, perimeter/2, op(700, xfx, ===>)]).
area(square(S), A) :- A is S*S.
```
- `module(+Module, +PublicList)` must be the first term of the file. PublicList items are `Name/Arity`, `Name//Arity` (DCG) or `op(Priority, Type, Name)`.
- Exported operators are defined inside the module and in every module that imports it.
- The module name is normally the file base name, but this is not enforced. If Module is unbound it is unified with the base name.
- A non-exported predicate is still callable as `shapes:helper(X)`.
- Predicates that take goals as arguments need `meta_predicate/1`.
## Gotchas
- `module/2` anywhere but first is an error.
- Two modules exporting the same name/arity cannot both be imported without resolving the conflict (see use_module/2 `except` and `as`).
## Self-check
Load the file, call `shapes:area(square(2), A)` and `area(square(2), A)` after importing it.

## Checked

2026-11-03. SWI-Prolog manual section on defining a module (module/2 first term, PublicList forms, operator export visible inside the module and to importers, base-name rule, unbound Module, `Module:Goal` qualification, meta-predicate note). Removed: "operators visible only in importers" (wrong), the library-by-file-name resolution example and the "existence error" self-check (not covered).

Method: documentation only; no commands were run.
