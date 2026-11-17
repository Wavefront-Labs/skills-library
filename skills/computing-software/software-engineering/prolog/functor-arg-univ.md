---
id: computing-software.software-engineering.prolog.functor-arg-univ
name: functor-arg-univ
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, functor-arg-univ, univ-operator]
level: practitioner
status: docs-checked
description: "Decompose and construct terms with functor/3, arg/3, =../2 and compound_name_arguments/3."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Taking terms apart
```prolog
?- functor(foo(a,b), N, A).        % N=foo, A=2
?- functor(T, point, 3).           % T = point(_,_,_)
?- arg(2, foo(a,b), X).            % X = b
?- foo(a,b) =.. L.                 % L = [foo,a,b]
?- T =.. [bar, 1, 2].              % T = bar(1,2)
?- compound_name_arguments(T, f, []).   % T = f() zero-arity compound (SWI-Prolog 7+)
```
## Gotchas
- `arg(N, T, A)` with unbound N enumerates arguments on backtracking; it fails silently for N = 0 or N above the arity.
- Zero-arity `f()` differs from the atom `f`: `functor/3` and `=..` raise a `domain_error` for it, so use `compound_name_arguments/3` or `compound_name_arity/3`.
## Self-check
Write `map_args(F, T0, T)` applying F to each argument of T0 using `=..` and `maplist`.

## Checked

2026-11-02. SWI-Prolog manual: functor/3 (skeleton term, atomic gives arity 0, zero-arity terms need functor/4 or compound_name_arity/3 and raise domain_error), arg/3 (enumerates with unbound Arg, fails silently at 0 or above arity), =../2 examples, compound_name_arguments/3. Removed: the unbound-list instantiation-error gotcha.

Method: documentation only; no commands were run.
