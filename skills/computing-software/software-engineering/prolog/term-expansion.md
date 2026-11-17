---
id: computing-software.software-engineering.prolog.term-expansion
name: term-expansion
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, term-expansion, goal-expansion]
level: sme
status: docs-checked
description: "Rewrite source with term_expansion/2 and goal_expansion/2 in SWI-Prolog and know the expand_term/2 order."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/man/builtin.plx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# term_expansion and goal_expansion
```prolog
:- multifile user:term_expansion/2.
:- dynamic user:term_expansion/2.
user:term_expansion(gen(N), [num(N), num(M)]) :- M is N+1.
gen(1).                                  % loads as num(1), num(2)
user:goal_expansion(old(X), new(X)).
```
- `term_expansion(+Term1, -Term2)` is dynamic and multifile. Term2 may be a list of clauses or a directive `:- Goal`.
- `expand_term/2` order: conditional compilation, `term_expansion` (module being compiled, then `user`, then `system`), DCG translation, then `goal_expansion` on clause bodies. Library modules inherit directly from `system`, so rules in `user` do not affect them.
- `goal_expansion/2` applies to goals that appear literally in clause bodies or as meta-arguments declared `0`.
- `begin_of_file` and `end_of_file` are also passed to `term_expansion`.
- `library(apply_macros)` expands `maplist` and related calls at compile time.
## Gotchas
- Expansion happens when a file is compiled; clauses added with `assert/1` are not passed through it.
## Self-check
Load a file containing `gen(1).` and list `num/1`.

## Checked

2026-11-03. SWI-Prolog manual section on term and goal expansion (expand_term/2 order, module search order, library modules inheriting from system, goal_expansion scope, begin_of_file / end_of_file, apply_macros). Removed: the claim that yall lambdas are expanded and the explicit statement that assert bypasses expansion (it is not stated in the pages read; the Gotcha above is limited to what the order of compilation implies).

Method: documentation only; no commands were run.
