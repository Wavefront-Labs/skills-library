---
id: computing-software.software-engineering.nim.pegs-grammar-matching
name: pegs-grammar-matching
category: computing-software
field: software-engineering
product: nim
tags: [pegs-grammar-matching, regex-and-pegs, pegs, peg, grammar, parsing-expression, peg-captures, replace, nim]
level: advanced
status: docs-checked
description: "Write parsing expression grammars with std/pegs for matching, captures and replacement as a readable alternative to regex."
sources:
  - https://nim-lang.org/docs/pegs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PEGs with std/pegs

Goal: use PEGs for structured matching.

- `import std/pegs`; build a peg: `let p = peg"{\ident} \s* '=' \s* {\d+}"`.
- Match: `if "x = 42" =~ p: echo matches[0], matches[1]`; `find`, `findAll`, `replacef(s, p, "$1")` (`replace` takes a plain replacement string; `replacef` expands `$1`), `split`.
- Syntax: `/` ordered choice, `*` zero or more, `+`, `?`, `&E` and `!E` predicates, `{...}` capture, `$i` back reference, `\ident`, `\d`, `\s`, character classes `[a-z]`, rules `Name <- expr` (left-recursive rules are not possible and crash the matching engine).
- A PEG is a deterministic grammar; ordered choice tries alternatives in order.

Gotchas:
- Ordered choice means order matters: put the longer alternative first.

Verify: grammar above captures the identifier and number.

## Checked

2026-11-03. Confirmed against the pegs page: peg syntax table (`/`, `*`, `+`, `?`, `&`, `!`, `{}`, `$i`, `[...]`, `<-`), built-in macros `\ident \d \s`, `=~`, find, findAll, split, replace and replacef. Real error fixed: `replace(s, p, "$1")` does not expand `$1`; `replacef` does. Removed: the npeg recommendation, the first-rule-is-start claim and the no-catastrophic-backtracking claim.

Method: documentation only; no commands were run.
