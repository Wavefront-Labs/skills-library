---
id: computing-software.software-engineering.erlang.case-if-expressions
name: case-if-expressions
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-expressions, case-if-expressions]
level: intro
status: docs-checked
description: "Erlang conditionals: case with patterns and guards, if with guard-only branches, and variable scoping across branches."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# case, if and receive expressions
**Goal:** choose the right conditional form.

```erlang
case lists:keyfind(id, 1, L) of
    {id, N} when N > 0 -> {ok, N};
    {id, _} -> {error, bad_id};
    false -> {error, missing}
end.

if X > 10 -> big; true -> small end.
```
- `if` branches are guards only; always include a final `true ->` or you risk `if_clause`.
- No match in `case` raises `{case_clause, Value}`.
- Variables bound in a branch are unsafe outside it unless bound in every branch.
- Prefer function clauses over nested `case` for readability.

## Gotchas
- Using `;` in an `if` guard is OR, not a separator for branches.

## Self-check
Force a `case_clause` and an `if_clause` in the shell.

## Checked
2026-11-02. Confirmed: system/expressions.html: if guard sequences and if_clause, case_clause, true as else branch, unsafe variables outside branches.
Removed: nothing removed.
Method: documentation only; no commands were run.
