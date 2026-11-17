---
id: computing-software.software-engineering.prolog.strings-vs-atoms
name: strings-vs-atoms
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, strings-vs-atoms, string-types]
level: practitioner
status: docs-checked
description: "Choose between atoms, SWI-Prolog strings, code lists and char lists and convert with atom_string/string_codes/text_to_string."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atoms vs strings vs codes
SWI-Prolog has a distinct `string` type; `"abc"` reads as a string by default (flag `double_quotes`; the default becomes `codes` with `--traditional`).
```prolog
?- string("abc").                    % true
?- atom_string(A, "abc").            % A = abc
?- string_codes(S, [104,105]).       % S = "hi"
?- text_to_string(hello, S).         % S = "hello"
?- atom_codes(abc, C).               % C = [97,98,99]
?- atom_chars(abc, C).               % C = [a,b,c]
```
Backquote text `` `abc` `` is a code list by default (flag `back_quotes`, default `codes`).
## Gotchas
- `"abc" == abc` fails; `"abc" = abc` fails: they are different types.
- Converting a number: `atom_number/2` fails silently if the atom is not a number; `number_string/2` also fails rather than raising a syntax error.
## Self-check
Evaluate `atom_length(abc, L)` and `string_length("abc", L)` and compare the results.

## Checked

2026-11-02. SWI-Prolog manual: double_quotes flag (default string, codes with --traditional; chars, atom), back_quotes flag (default codes), atom_string/2, string_codes/2, text_to_string/2, atom_codes/2, atom_chars/2, atom_number/2, number_string/2. Removed: the DCG literal note and the atom_length unbound prediction (not read).

Method: documentation only; no commands were run.
