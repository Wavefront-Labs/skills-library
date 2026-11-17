---
id: computing-software.software-engineering.prolog.type-test-predicates
name: type-test-predicates
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-typecheck, type-test-predicates, var-nonvar]
level: intro
status: docs-checked
description: "Test terms with var/1, nonvar/1, atom/1, number/1, integer/1, atomic/1, compound/1, callable/1, is_list/1 and must_be/2."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type tests
```prolog
?- var(X).  ?- nonvar(a).  ?- atom([]).   % false in SWI-Prolog 7+
?- atomic("s").  ?- compound(f(x)).  ?- callable(foo).  ?- is_list([a|_]).  % false
:- use_module(library(error)).
check(N) :- must_be(positive_integer, N).    % throws type_error(positive_integer, N)
```
## Gotchas
- `atom([])` is false in SWI-Prolog 7+ (`[]` is a reserved constant); `atomic([])` is true.
- Type tests never bind; they cannot replace unification.
- `must_be/2` raises `instantiation_error` for insufficiently instantiated input and `type_error(Type, Term)` otherwise; `is_of_type/2` is semidet.
## Self-check
Run `must_be(integer, foo)` and `must_be(integer, _)`; compare the error terms.

## Checked

2026-11-02. SWI-Prolog manual: atom/1, callable/1 (atom or compound, surface test only), is_list/1, the reserved constant [] (atom([]) fails, atomic([]) succeeds); library(error) source for must_be/2 (type_error(Type, Term), instantiation_error) and is_of_type/2 (semidet). Fixed: must_be raises type_error, not domain_error, in the library source.

Method: documentation only; no commands were run.
