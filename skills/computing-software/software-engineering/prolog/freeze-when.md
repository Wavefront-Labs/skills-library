---
id: computing-software.software-engineering.prolog.freeze-when
name: freeze-when
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, freeze-when, coroutining]
level: advanced
status: docs-checked
description: "Delay goals with freeze/2 and when/2, and inspect them with frozen/2 in SWI-Prolog coroutining."
sources:
  - https://www.swi-prolog.org/pldoc/man?predicate=freeze/2
  - https://www.swi-prolog.org/pldoc/man?predicate=frozen/2
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/library/when.pl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Coroutines
```prolog
?- freeze(X, writeln(got(X))), X = 1.          % prints got(1)
?- freeze(X, true), frozen(X, G).              % G describes the delayed goal
?- when(ground(f(X,Y)), writeln(done)), X = 1, Y = 2.
?- when((nonvar(X);nonvar(Y)), writeln(one_bound)).
?- when(?=(X,Y), writeln(decided)).
```
- `freeze(+Var, :Goal)` delays Goal until Var is bound; if Var is already bound it equals `call/1`.
- `frozen(@Term, -Goal)` reports all delayed goals on the variables of Term (as `copy_term/3` does) and is true with `true` when none.
- `when(@Cond, :Goal)` conditions: `nonvar(X)`, `ground(X)`, `?=(X,Y)` (X and Y are identical or cannot unify), and combinations with `,` and `;`. It lives in library(when) and is autoloaded.
## Gotchas
- A delayed goal that never fires is silent; check with `frozen/2`.
## Self-check
`freeze(X, fail), X = 1` must fail.

## Checked

2026-11-03. SWI-Prolog manual freeze/2, frozen/2 and library(when) when/2 documentation (when.pl in swipl-devel): condition forms and meanings, autoloading. Removed: wakeup-order guarantees, claims about where exceptions surface and how the toplevel formats residual goals.

Method: documentation only; no commands were run.
