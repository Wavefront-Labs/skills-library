---
id: computing-software.software-engineering.clojure.clojure-version-feature-timeline-1-9-to-1-12
name: clojure-version-feature-timeline-1-9-to-1-12
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, clojure-versions, 1.10, 1.11, 1.12, iterate, parse-long, update-vals, stream-reduce, method-values, release-notes, version-features-1-11-1-12]
level: practitioner
status: docs-checked
description: "Know which features arrive in which Clojure version: spec (1.9), tap and ex-message (1.10), parse-long, update-vals and clojure.math (1.11), qualified methods (1.12)."
sources: ["https://clojure.org/news/news", "https://github.com/clojure/clojure/blob/master/changes.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clojure version feature timeline

**Goal:** know what you can use on the Clojure version your project targets.

- 1.9: `clojure.spec.alpha`, `int?`/`pos-int?`/`any?`, `qualified-keyword?`, `halt-when`, `##Inf`/`##NaN`
  literals (the socket server arrived in 1.8).
- 1.10: `tap>`/`add-tap`, `ex-message`/`ex-cause`, protocol extension by metadata (`:extend-via-metadata`), `datafy`/`nav`
  (`clojure.datafy`), `prepl` (alpha), improved error messages, a read-string capture mode.
- 1.11: `parse-long`, `parse-double`, `parse-boolean`, `parse-uuid`, `random-uuid`, `update-keys`, `update-vals`,
  `iteration`, `clojure.math` namespace, `:as-alias` in `require`, kwargs functions accept a trailing map, `abs`.
- 1.12: qualified method values (`String/length`, `Math/abs` usable as first-class fns), array class syntax
  (`String/1`), functional interface adaptation (passing Clojure fns where Java functional interfaces are
  expected), `add-lib`/`add-libs`/`sync-deps` for REPL dependency loading, the `clojure.java.process` namespace,
  and lazy-seqs and delays no longer pin threads under JDK 21 virtual threads.
- Always read the official `changes.md` for exact version numbers before relying on a function in a library
  that supports multiple Clojure versions.
- When upgrading, run the test suite: 1.11.0 added `abs` to `clojure.core`, which broke code compiled against an earlier Clojure that had its own `abs` var (fixed in later 1.11.x releases).

## Failure modes
- Using `parse-long` in a library that must support 1.10 (it will fail to resolve).
- Assuming a feature exists because the REPL docs show it, while production runs an older jar.

## Self-check
Print `(clojure-version)` and use `(resolve 'parse-long)` to check presence at runtime.

## Checked
2026-11-03. Confirmed against changes.md (sections for 1.8, 1.9, 1.10, 1.11, 1.12) and the clojure.core and clojure.repl API pages ("Added in" versions of the listed functions: 1.9 int?/pos-int?/any?/qualified-keyword?/halt-when; 1.10 tap>/add-tap/ex-message/ex-cause; 1.11 parse-*, random-uuid, update-keys, update-vals, iteration, abs, :as-alias, trailing-map kwargs, clojure.math; 1.12 qualified methods, array class syntax, functional interfaces, add-lib/add-libs/sync-deps, clojure.java.process). Fixed: prepl is a 1.10 feature, not 1.9; the 1.12 virtual-thread item concerned lazy-seqs and delays, not executors. Removed: `clojure.main -e` and `:read-cond` items, and the backward-compatibility policy sentence (not in the pages read).
Method: documentation only; no commands were run.
