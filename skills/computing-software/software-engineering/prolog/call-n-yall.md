---
id: computing-software.software-engineering.prolog.call-n-yall
name: call-n-yall
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, call-n-yall, yall-lambda, swi-prolog, lambda]
level: practitioner
status: docs-checked
description: "Build closures with call/N and library(yall) lambdas: Params>>Goal, {Free}/Params>>Goal, the copy-term rule and shared variables."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/library/yall.pl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# call/N and yall

`call(G, A1, ...)` calls closure `G` with extra arguments appended to the end of its argument list. A closure is a term whose arguments are the leftmost arguments of a predicate: `call(atom_concat(prefix), suffix, R)` and `call(atom_concat, prefix, suffix, R)` are equivalent.

Problem: arguments are only appended, so `maplist(atom_concat(Postfix), In, Out)` calls `atom_concat(Postfix, In, Out)`, the wrong order for adding a postfix. library(yall) ("Yet Another Lambda Library") fixes that without helper predicates.

```prolog
:- use_module(library(yall)).
?- maplist([In,Out]>>atom_concat(In,'_p',Out), [a,b], L).      % L = [a_p, b_p]

add_postfix(Postfix, ListIn, ListOut) :-
    maplist({Postfix}/[In,Out]>>atom_concat(In,Postfix,Out), ListIn, ListOut).
```

## Syntax (module header comment)
`{Free}/[Params]>>Goal`
- `[Params]` is a list; order matters. Parameters are unified positionally with the call arguments; excess arguments are passed on to the goal by position.
- `{Free}` is optional: the variables shared between the lambda and the surrounding context (a set, order does not matter). Without `{Postfix}` in the example above, a fresh variable would be passed to `atom_concat/3`.
- `/` and `>>` are standard infix operators; the library adds none. A lambda can be unified with `{Free}/[Params]>>Lambda` to take it apart. The goal may need parentheses, and module-qualified goals must be parenthesised.
- `Free/Lambda` on its own (`/`/2..9) is shorthand for `Free/[]>>Lambda`: it calls a copy of the closure but only variables in `Free` are bound by the call.

## Copy semantics
- `>>` calls a copy of the lambda term (`copy_term_nat`). Variables not listed in `{Free}` are therefore copied, and the body does not bind the outer variable. Outer variables that are already bound when the lambda is called (for example `N = 10` before `maplist`) are copied as their values, so they work without `{N}`.
- To get a binding out of the body, list the variable in `{...}`.
- `{X}/p(X,Y)` selects the variables of interest, the converse of `^`: `setof(X, Y^p(X,Y), Xs)` and `setof(X, {X}/p(X,_), Xs)` are equivalent.
- `{Free}` must be `{}` or a braced term; anything else raises `type_error(lambda_free, _)`; an unbound lambda parameter list raises an instantiation error; more parameters than call arguments raises `domain_error(lambda_parameters, _)`.

## Compilation
- yall defines `system:goal_expansion/2`: when a source file is loaded and a lambda is sufficiently instantiated, it is compiled to an auxiliary predicate named `__aux_yall_<hash>`. Free variables are passed as extra arguments.
- Combined with library(apply_macros), yall allows list one-liners with the same performance as hand-written code, per the module documentation.
- Utility predicates: `is_lambda/1`, `lambda_calls/2,3` (used for cross-referencing and highlighting).

## Self-check
`N = 5, maplist([X,Y]>>(Y is X+N), [1,2], L)` gives `L = [6,7]`: `N` is bound before the call, so its copy keeps the value 5.

## Checked

Method: 2026-11-08 read library/yall.pl from the SWI-Prolog repository (export list, module comment, pldoc and clause bodies, about 85 percent of the file; the sandbox declarations at the end were not read). Removed claims the source does not support: the `\X^` local-parameter form, the "slower interpretation if loaded late" remark and the `Mod:Goal` note for dynamic predicates. The manual landing page and metalevel.at sources were dropped as unread. Documentation only; no commands were run.
