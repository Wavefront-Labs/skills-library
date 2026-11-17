---
id: computing-software.software-engineering.prolog.toplevel-features
name: toplevel-features
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, toplevel-features, init-pl]
level: intro
status: draft
description: "Use the interactive toplevel: query variable bindings, ;, history, $Var, init.pl and prolog flags answer_write_options."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Toplevel features
- `?- X = 1.` prints bindings; `;` next, `a` all, `w` write, `p` print, `c` stop.
- `$X` refers to bindings from the previous query: `?- X = 1.` then `?- Y is $X + 1.`
- `?- [user].` enter clauses; `listing.`; `halt.` or Ctrl-D exits.
- Init file: `~/.config/swi-prolog/init.pl` (Linux), `%APPDATA%/swi-prolog/init.pl` (Windows).
- `set_prolog_flag(answer_write_options, [max_depth(0)])` prints long lists in full.
- `edit(foo)`, `make.`, `shell(ls)`.
## Gotchas
- Toplevel variables persist only through `$Var`, not as real variables.
- `_` variables are not printed unless `toplevel_print_anon` is true.
## Self-check
Set max_depth to 0 and print `numlist(1, 50, L)`.
