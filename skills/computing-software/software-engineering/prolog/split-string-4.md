---
id: computing-software.software-engineering.prolog.split-string-4
name: split-string-4
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, split-string-4, atomic-list-concat]
level: intro
status: docs-checked
description: "Tokenise and transform text with split_string/4, string_concat/3, sub_string/5, atomic_list_concat/3, string_code/3."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String helpers
```prolog
?- split_string("a,b,,c", ",", "", P).          % ["a","b","","c"]
?- split_string("  hi  ", "", " ", [T]).        % T = "hi" (strip)
?- atomic_list_concat(Parts, ',', 'a,b,c').     % split mode: Parts=[a,b,c]
?- atomic_list_concat([a,b,c], '-', R).          % join: 'a-b-c'
?- sub_string("hello world", B, _, 0, "world"). % B = 6
?- string_upper("abc", U), string_concat(U, "!", R).
?- number_string(N, "42").                        % N = 42
```
## Gotchas
- `atomic_list_concat/3` split mode (`-,+,+`) needs a non-empty atom separator; `number_string/2` fails (no syntax error) if the string is not a number and does not allow leading white space.
- `split_string` returns strings; the pad argument strips each part.
- `sub_string/5` is functionally equivalent to `sub_atom/5` but returns strings.
## Self-check
Split a CSV line, trim fields, and convert numeric ones via `number_string/2`.

## Checked

2026-11-02. SWI-Prolog manual string predicates: split_string/4 (separators, pad characters, ECLiPSe compatible), atomic_list_concat/3 (join, and split mode needing a non-empty separator), sub_string/5, string_upper/2, number_string/2 (fails on non-numbers; leading white space not allowed). Fixed: number_string example with surrounding spaces. Removed: the sub_atom enumeration advice.

Method: documentation only; no commands were run.
