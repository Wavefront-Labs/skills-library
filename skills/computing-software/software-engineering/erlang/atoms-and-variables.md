---
id: computing-software.software-engineering.erlang.atoms-and-variables
name: atoms-and-variables
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-lexical, atoms-and-variables]
level: intro
status: docs-checked
description: "Erlang atom and variable syntax: quoting rules, single assignment, the anonymous variable and the atom table limit."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atoms and variables
**Goal:** write correct atoms and variables and avoid atom-table exhaustion.

- Atoms start lowercase or are single-quoted: `ok`, `'Hello World'`, `'GET'`. The atom table is bounded.
- Variables start uppercase or `_`: `Count`, `_Ignored`, `_`. `_` never binds; `_Name` binds but silences the unused warning.
- Variables are single assignment per scope; a second `X = ...` is a match, not a rebind.
```erlang
1> X = 1.
1
2> X = 2.
** exception error: no match of right hand side value 2
3> f(X).          % shell only: forget a binding
ok
```
- The default maximum number of atoms is 1,048,576; see the system limits page for the emulator flag that changes it.
- `true` and `false` are ordinary atoms; there is no separate boolean type.

## Gotchas
- `list_to_atom/1` on external input can exhaust the atom table and crash the VM; use `list_to_existing_atom/1` or keep binaries.
- A variable bound inside only one branch of `case` is "unsafe" and cannot be used after the `case`.

## Self-check
In the shell, bind `X = 1`, confirm `X = 2` fails, then `f(X)` and rebind.

## Checked
2026-11-02. Confirmed: system/expressions.html: variables start uppercase or underscore, single assignment, badmatch; system/system_limits.html: atom limit 1,048,576.
Removed: Never-garbage-collected claim, erl +t flag and system_info keys (not stated in pages read).
Method: documentation only; no commands were run.
