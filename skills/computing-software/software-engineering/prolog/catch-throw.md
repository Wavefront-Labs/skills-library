---
id: computing-software.software-engineering.prolog.catch-throw
name: catch-throw
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-exceptions, catch-throw, exception-handling]
level: practitioner
status: docs-checked
description: "Raise and handle exceptions with throw/1 and catch/3, re-throw unmatched ones, and know that bindings are undone."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# catch/3 and throw/1
```prolog
?- catch(X is 1/0, error(E, _), (print_message(error, E), fail)).
safe_div(A, B, R) :-
    catch(R is A / B, error(evaluation_error(zero_divisor), _), R = inf).
check(X) :- ( X > 0 -> true ; throw(my_error(bad_value(X))) ).
?- catch(check(-1), my_error(Why), format("caught ~w~n", [Why])).
```
- `catch(Goal, Catcher, Recovery)`: if Goal throws a ball that unifies with Catcher, the choice points of Goal are cut, execution backtracks to the start of `catch/3` and Recovery is called as `call/1`.
- Unmatched balls propagate outward.
## Gotchas
- A variable catcher matches every ball, including `unwind(halt(Status))` (raised by `halt/1`); catch specific patterns.
- `throw/1` copies the ball (SWI-Prolog delays the copy-and-backtrack until a matching `catch/3` is found).
## Self-check
Throw a custom ball, catch it two frames up, and confirm an inner non-matching catch re-throws it.

## Checked

2026-11-02. SWI-Prolog manual: catch/3 (innermost matching catcher, choice points cut, Recover called as call/1), throw/1 (ball copied, backtracking delayed until a catch is found), halt/1 (raises unwind(halt(Status))), exception ordering list. Removed: the directive-warning line (not read in the fetched sections).

Method: documentation only; no commands were run.
