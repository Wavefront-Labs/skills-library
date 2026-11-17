---
id: computing-software.software-engineering.prolog.setarg-mutable
name: setarg-mutable
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, setarg-mutable, nb-setarg]
level: sme
status: docs-checked
description: "Mutate compound term arguments with backtrackable setarg/3 and destructive nb_setarg/3 for efficient counters and accumulators."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Destructive term updates
```prolog
?- T = count(0), forall(member(_, [a,b,c]), (arg(1, T, N), N1 is N+1, nb_setarg(1, T, N1))), arg(1, T, V).   % V = 3
?- T = f(a), setarg(1, T, b), arg(1, T, X).      % b, undone on backtracking
```
- `setarg/3` is undone on backtracking; `nb_setarg/3` is not reversed on backtracking and duplicates a non-atomic value (`duplicate_term/2`); `nb_linkarg/3` does not duplicate.
- Idiom (from the `nb_setarg/3` entry): `Counter = counter(0), ( Goal, arg(1, Counter, N0), N is N0+1, nb_setarg(1, Counter, N), fail ; arg(1, Counter, Times) )`.
## Gotchas
- The manual calls `setarg/3` extra-logical and says to avoid it where possible, because of unexpected copying and non-copying of terms. Its advice: give a term whose arguments are updated one extra unused, unshared variable, so `copy_term/2` does not share it and the term counts as non-ground. `put_attr/3` is the alternative.
- `nb_setarg/3` with a counter term created in the clause body (`Counter = counter(0)`) is the manual's thread-safe, reentrant way to count solutions.
## Self-check
Write `max_in_findall/2` with `nb_setarg` and compare with `max_list`.

## Checked

2026-11-02. SWI-Prolog manual entries setarg/3 (backtrackable, extra-logical, advice on an unused unshared variable, put_attr/3), nb_setarg/3 (not reversed, duplicate_term for non-atomic values, succeeds_n_times example) and nb_linkarg/3. Removed: the claim that changing shared or asserted terms is undefined and the copy_term advice for clause literals (not stated).

Method: documentation only; no commands were run.
