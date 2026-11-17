---
id: computing-software.software-engineering.prolog.sub-atom-5
name: sub-atom-5
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, sub-atom-5, atom-concat]
level: practitioner
status: docs-checked
description: "Search, split and slice atoms with sub_atom/5, atom_concat/3 (enumerating splits) and atomic_list_concat/3."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sub_atom/5
`sub_atom(+Atom, ?Before, ?Length, ?After, ?Sub)` enumerates substrings.
```prolog
?- sub_atom(hello, 1, 3, _, S).          % S = ell
?- sub_atom(hello, B, _, 0, llo).        % B = 2, suffix test
?- sub_atom(hello_world, B, _, _, '_').  % find separator
?- atom_concat(X, Y, ab).                % X='',Y=ab ; a,b ; ab,''
?- atom_concat(abc, X, abcdef).          % X = def (prefix removal)
```
## Gotchas
- Leaving Before, Length and After unbound enumerates all sub-atoms on backtracking; constrain at least some of them.
- `sub_atom/5` is flexible (search, prefix and suffix matching) and minimises non-determinism and atom creation; when you generate many short-lived atoms the manual suggests `sub_string/5`.
- `sub_string/5` is the string-typed variant.
## Self-check
Implement `starts_with(Atom, Prefix)` using `sub_atom/5` without enumeration.

## Checked

2026-11-02. SWI-Prolog manual: sub_atom/5 (0-based Before, Length, After; search, prefix and suffix matching; sub_string/5 as alternative for short-lived atoms), atom_concat/3 (mode -,-,+ splits non-deterministically). Removed: the O(n^2) figure and the atom table claim.

Method: documentation only; no commands were run.
