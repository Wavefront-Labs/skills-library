---
id: computing-software.software-engineering.prolog.use-module-import
name: use-module-import
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, use-module-import, reexport]
level: practitioner
status: docs-checked
description: "Import with use_module/1,2, rename or exclude predicates, reexport and understand weak imports and the autoload flag."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/man/module.plx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# use_module and imports
```prolog
:- use_module(library(lists)).
:- use_module(library(lists), [append/3, last/2 as final]).
:- use_module(library(lists), except([flatten/2])).
:- reexport(library(pairs)).               % must directly follow the module declaration
```
- `use_module/1` is like `ensure_loaded/1` but raises an error if the file is not a module file.
- `use_module/2` takes an import list: `Name/Arity`, `Name/Arity as NewName`, or `except(List)`.
- `reexport/1,2` must immediately follow the module declaration.
- Imports behave as weak symbols: a local definition overrides the import with a warning such as "Local definition of shapes:flatten/2 overrides weak import from lists". The flag `warn_override_implicit_import` controls it (default true).
- Importing the same name/arity from two modules gives "No permission to import ... already imported from".
- The flag `autoload` takes `false`, `explicit`, `user`, `user_or_explicit` or `true` (default).
## Gotchas
- Prefer an explicit import list for non-library modules to avoid clashes.
## Self-check
Define `flatten/2` locally after `use_module(library(lists))` and read the warning.

## Checked

2026-11-03. SWI-Prolog manual: use_module/1,2, import list forms, reexport/1,2, section on overruling imports (weak import message and flag), import-conflict message, flag autoload values. Removed: make/0 remarks and the claim that overrides are silent for libraries.

Method: documentation only; no commands were run.
