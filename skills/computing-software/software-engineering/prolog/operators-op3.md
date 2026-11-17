---
id: computing-software.software-engineering.prolog.operators-op3
name: operators-op3
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, operators-op3, op-3]
level: practitioner
status: docs-checked
description: "Define and inspect operators with op/3: priority, xfx/xfy/yfx types, and how operator terms parse into canonical form."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operators and op/3
`op(+Precedence, +Type, :Name)`: precedence 0-1200 (0 removes the declaration), type one of `xf yf xfx xfy yfx fy fx`.
```prolog
:- op(700, xfx, ===>).
:- op(200, xfy, ^).        % right associative, built in
?- current_op(P, T, mod).  % P=400, T=yfx
?- X = 1-2-3, X = A-B.    % A = 1-2, B = 3, since - is yfx
```
## Gotchas
- Operators are local to a module; export them in the `module/2` export list to share them. The system operators cannot be modified, and redefining operators can change how other files are read.
- Comma is `op(1000, xfy, ',')` and cannot be redefined; the bar `|` can only be an infix operator with priority 1001 or more.
## Self-check
Define `:- op(700, xfx, is_bigger).` then write a fact `elephant is_bigger mouse.` and query it with `X is_bigger Y`.

## Checked

2026-11-02. SWI-Prolog manual op/3 entry (precedence 0-1200, 0 removes, types xf yf xfx xfy yfx fy fx), the system operator table (mod 400 yfx, ^ 200 xfy, comma 1000 xfy, - 500 yfx), restrictions (comma, bar), module-local operators. Removed: the write_canonical outputs, the argument-priority and prefix-atom gotchas (not read).

Method: documentation only; no commands were run.
