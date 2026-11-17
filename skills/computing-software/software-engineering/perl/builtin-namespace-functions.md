---
id: computing-software.software-engineering.perl.builtin-namespace-functions
name: builtin-namespace-functions
category: computing-software
field: software-engineering
product: perl
tags: [perl, builtin-namespace, builtin-true-false, builtin-trim, is-bool, indexed-builtin, builtin-namespace-functions]
level: advanced
status: docs-checked
description: "Use builtin:: functions (true, false, is_bool, trim, ceil, floor, reftype, blessed, indexed, refaddr, weaken) and know their stability by version."
sources: ["https://perldoc.perl.org/builtin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The builtin:: namespace

**Goal:** core replacements for small utility functions.

```perl
use builtin qw(true false is_bool trim ceil floor blessed refaddr reftype weaken indexed created_as_number);
# many builtin functions warn under the experimental::builtin category; see perldoc builtin
my $flag = true;                              # real boolean values
say is_bool($flag) ? 'bool' : 'not';          # true for results of comparisons and true/false
say trim("  padded \n");                      # removes leading/trailing whitespace
say ceil(1.2), floor(-1.2);
for my ($i, $v) (indexed @list) { say "$i: $v" }     
```

## Details (check `perldoc builtin` for your Perl)
- Many functions in the namespace are still experimental and warn under category `experimental::builtin`. Version bundles (`use builtin ':5.40'`) import the set considered stable by that release; for `:5.40` perldoc builtin lists `true false weaken unweaken is_weak blessed refaddr reftype`. Check `perldoc builtin` for your Perl.
- Import is lexical: `use builtin 'trim'` makes `trim` visible only in the enclosing scope (no symbol-table pollution); you can also call `builtin::trim(...)` fully qualified without importing.

## Rules
- Pin the minimum Perl in metadata when using them.
- Don't rely on experimental builtins in released distributions without version guards.
- Prefer imports at the top of each file for clarity.

## Self-check
- [ ] `perl -E 'use builtin qw(trim); say "[", trim("  x "), "]"'` prints `[x]` on a Perl that has `builtin::trim`.

## Checked
2026-11-02: confirmed against perldoc builtin (function list incl. trim, ceil, floor, indexed; experimental status and experimental::builtin warnings; version bundles and the :5.40 contents; lexical import). Removed: release-by-release history, boolean-ness remarks, C-implementation remark.
Method: documentation only; no commands were run.
