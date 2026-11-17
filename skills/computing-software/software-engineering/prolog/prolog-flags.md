---
id: computing-software.software-engineering.prolog.prolog-flags
name: prolog-flags
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-iso, prolog-flags, double-quotes-flag]
level: practitioner
status: docs-checked
description: "Inspect and set flags with current_prolog_flag/2 and set_prolog_flag/2: double_quotes, occurs_check, unknown, iso, verbose."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prolog flags
```prolog
?- set_prolog_flag(double_quotes, codes).       % maintained per module
?- set_prolog_flag(occurs_check, true).
?- set_prolog_flag(unknown, fail).               % undefined procedures fail silently (careful)
?- set_prolog_flag(iso, true).                   % stricter ISO behaviour
?- current_prolog_flag(bounded, B).
```
- `double_quotes` values: `codes`, `chars`, `atom`, `string` (default `string`; `codes` with `--traditional`).
- Only `generate_debug_info` and `optimise` are scoped to the source file; a new thread copies the flags of its parent.
## Gotchas
- `unknown` is `error` by default (existence_error); `fail` makes undefined procedures fail silently, which hides typos.
- The `iso` flag changes `/` (always a float), the standard order of terms (all floats before integers), `atom_length/2` type errors and more: test before switching.
## Self-check
Set `double_quotes` to `codes` in a directive and check that `"ab" = [97,98]` when read after it.

## Checked

2026-11-02. SWI-Prolog manual flags section: double_quotes (codes, chars, atom, string; default string; per module), unknown (default error, fail), occurs_check (false default, true, error), iso (float division, standard order, atom_length), bounded, scoping of flags to source files (generate_debug_info, optimise), threads copy flags. Removed: the version flag example and the per-file claim for double_quotes (the manual says per module).

Method: documentation only; no commands were run.
