---
id: computing-software.software-engineering.clojure.conditionals-cond-case-condp-when-let
name: conditionals-cond-case-condp-when-let
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, conditionals, cond, case, condp, if-let, when-let, when-some, if-some, cond-threading, cond-case-condp, clojure-control-flow]
level: intro
status: docs-checked
description: "Branch with if, when, cond, case (constant dispatch), condp, if-let, when-let and if-some; know truthiness, :else and case's compile-time constants."
sources: ["https://clojure.org/guides/learn/flow"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditionals

**Goal:** choose the right branching form.

```clojure
(cond (< n 0) :neg (zero? n) :zero :else :pos)       ; :else is just a keyword, always true
(case x 1 :one 2 :two :other)                        ; literal constants only; trailing expression is the default
(if (pos? n) :pos)                                   ; else is optional, yields nil
(when (neg? n) (log n) :neg)                         ; if with only a then branch, any number of body forms
```
- `case` compares in constant (not linear) time, so each test value must be a compile-time literal (numbers, strings, keywords). With no match and no trailing default it throws `IllegalArgumentException` ("No matching clause"); `cond` returns nil instead.
- `cond` has no built-in default; end with `:else` (keywords always evaluate to true).
- Only `nil` and `false` are logically false; everything else, including `0` and `""`, is true.
- `if` takes a single expression for each branch; use `do` for several.

## Failure modes
- Using `case` with runtime values instead of literals.
- Forgetting `cond` returns nil when no test matches.

## Self-check
`(cond false 1)` returns nil; `(case 5 1 :x)` throws `IllegalArgumentException`.

## Checked

2026-11-02. Checked against the Clojure guide 'Flow control' (clojure.org/guides/learn/flow): if with optional else, only nil and false are logically false, when, cond returning nil when nothing matches, :else idiom, case in constant time with compile-time literals, IllegalArgumentException on no match, case trailing default. Removed (not on that page): condp, if-let, when-let, if-some, when-not, when-first, if-not, case list grouping and the jump-table and symbol-matching remarks.

Method: documentation only; no commands were run.
