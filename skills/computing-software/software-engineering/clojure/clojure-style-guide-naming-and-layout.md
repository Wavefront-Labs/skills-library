---
id: computing-software.software-engineering.clojure.clojure-style-guide-naming-and-layout
name: clojure-style-guide-naming-and-layout
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, style-guide, naming, idioms, kebab-case, predicates, indentation, bbatsov, style-guide-naming-layout, clojure-style-lint]
level: practitioner
status: docs-checked
description: "Apply community Clojure Style Guide conventions: kebab-case names, ? and ! suffixes, earmuffs, 2-space indentation, blank lines, ns layout and common idioms."
sources: ["https://github.com/bbatsov/clojure-style-guide"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clojure style: naming and layout

**Goal:** write code that matches community norms so tools and readers agree.

- Names: `lisp-case` (kebab-case) for functions and vars; `CapitalCase` for protocols, records, structs and
  types (acronyms stay uppercase, `XMLParser`); predicates end in `?` and return only a boolean
  (`palindrome?`); functions with side effects that are unsafe in STM transactions end in `!` (`save-user!`);
  conversions use `->` not `to` (`f->c`); dynamic vars use earmuffs `*a*`; constants have no special notation
  (`max-size`); use `_` for ignored destructuring targets and arguments.
- Indentation: 2 spaces for bodies of `def` forms, special forms and body-taking macros; vertically align
  multi-line function arguments (single space if none share the first line); align `let` bindings and map
  keys; align each multi-arity form with its parameters.
- Put trailing parentheses on one line (rich `comment` blocks are an exception).
- Avoid lines over 80 characters where feasible (teams may go to 100 or 120).
- One blank line between top-level forms (except to group related `def`s); none inside definitions except to
  separate pairs in `let` or `cond`; no trailing whitespace.
- `ns` form order: refer, require, import (conventionally); sort requirements and imports, one per line;
  prefer `:require :as` over `:require :refer`, and `:refer` over `:refer :all` (acceptable as warranted);
  `:use` is deprecated for new code.
- Idioms: `when`/`when-not`/`if-not` for a single branch; `if-let`/`when-let` over `let` plus `if`/`when`;
  `not=` over `(not (= ...))`; `seq` as the emptiness test (the guide notes `empty?` is more efficient for
  counted collections on Clojure 1.12+); `->`/`->>` over deep nesting.
- Do not shadow `clojure.core` names with locals; do not define vars inside functions.

## Self-check
Review a file against this list, then let cljfmt/clj-kondo catch what you missed.

## Checked
Method: 2026-11-08 read the bbatsov/clojure-style-guide GitHub page; the fetched content was truncated, so later sections were not seen. guide.clojure.style was not read and was removed from sources. Removed claims the visible text did not state: `-main`, `defn-`, docstring placement, keywords-as-functions, requiring `~80` columns, ns alias conventions (str, set, io, walk), small-functions advice, and the `inc`/`dec`/`zero?` idioms.
