---
id: computing-software.software-engineering.prolog.indexing-last-call
name: indexing-last-call
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-performance, indexing-last-call, tail-recursion]
level: advanced
status: docs-checked
description: "Understand SWI-Prolog just-in-time clause indexing, jiti_list/0,1, last-call optimisation in debug mode and stack_limit."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/man/overview.plx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Indexing and last-call
```prolog
?- jiti_list.                       % library(prolog_jiti): show indexes
?- jiti_list(foo/3).
?- statistics(localused, N).
?- set_prolog_flag(stack_limit, 2_000_000_000).
```
- Just-in-time indexing builds an index on first call for whichever argument is instantiated; multiple arguments can be indexed.
- The principal clause list key is normally the first argument; with fewer than 10 clauses a linear scan is used.
- Compound arguments are indexed deeply.
- For dynamic predicates the index is discarded when the clause count doubles or drops below a quarter.
- `jiti_list/0,1` (library(prolog_jiti)) show the indexes; flags with prefix `ci_` tune clause indexing.
- Debug mode disables last-call optimisation.
- The stack limit is set by `--stack-limit` or the flag `stack_limit` (default 1Gb combined on 64-bit).
## Gotchas
- Indexes are built on demand at the first call, so the first call with a new instantiation pattern pays the build cost.
## Self-check
Run `jiti_list(foo/3)` before and after calling `foo/3` with a different argument bound and compare the listed indexes.

## Checked

2026-11-03. SWI-Prolog manual sections on just-in-time clause indexing (JITI), deep indexing, prolog_jiti library, the debugger page (last-call optimisation off in debug mode), and command-line / flag documentation for stack_limit. Removed: unconfirmed conditions for when last-call optimisation applies, "put the discriminating argument first" and the self-check based on error behaviour.

Method: documentation only; no commands were run.
