---
id: computing-software.software-engineering.prolog.atom-codes-chars
name: atom-codes-chars
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-atom-text, atom-codes-chars, atom-number]
level: intro
status: docs-checked
description: "Convert between atoms, numbers, code lists and char lists with atom_codes/2, atom_chars/2, atom_number/2, char_code/2, upcase_atom/2."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atom conversion
```prolog
?- atom_codes(hello, C).        % [104,101,108,108,111]
?- atom_chars(X, [h,i]).        % X = hi
?- atom_number('42', N).        % N = 42 ; fails silently for 'abc'
?- atom_number(A, 7).           % A = '7'
?- char_code(C, 0'a).           % C = a ; 0'a is the code literal 97
?- upcase_atom('hi there', U).  % 'HI THERE'
?- term_to_atom(f(X,Y), A).     % quoted atom of term
```
## Gotchas
- `atom_length/2` accepts all atomic types (`atom_length(123, L)` gives 3), as well as code and character lists.
## Self-check
Convert `'3.14'` to a number and back, and confirm the atom round-trips.

## Checked

2026-11-02. SWI-Prolog manual section on atoms and text conversion: atom_codes/2 (example hello gives [104,101,108,108,111]), atom_chars/2, char_code/2, atom_number/2 (fails silently in mode +,- if the atom is not a number), atom_length/2 (accepts all atomic types), upcase_atom/2, term_to_atom/2 (quoted write). Removed: the 0'' quote note and the atom_number unbound-both claim (not stated).

Method: documentation only; no commands were run.
