---
id: computing-software.software-engineering.clojure.numeric-types-ratios-bigdecimal-and-overflow
name: numeric-types-ratios-bigdecimal-and-overflow
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, numbers, ratio, bigint, bigdecimal, overflow, unchecked-math, auto-promoting, long, double, numeric-tower-overflow, clojure-numbers]
level: practitioner
status: docs-checked
description: "Handle Clojure numeric types: long, double, ratios, BigInt, BigDecimal; overflow behaviour of + vs +', unchecked ops, equality (= vs ==) and rounding."
sources: ["https://clojure.org/reference/data_structures#Numbers", "https://clojure.org/guides/equality", "https://clojure.github.io/clojure/clojure.core-api.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numeric types and overflow

**Goal:** avoid silent precision and overflow bugs.

```clojure
(/ 1 3)            ;=> 1/3 (ratio)       (double 1/3)  (/ 1.0 3)
(+ Long/MAX_VALUE 1)    ; throws java.lang.ArithmeticException (overflow)
(+' Long/MAX_VALUE 1)   ; auto-promotes to BigInt (9223372036854775808N)
(unchecked-add Long/MAX_VALUE 1)  ; primitive operator subject to overflow
(bigint 5)  (bigdec "0.1")  (+ 0.1M 0.2M)  ;=> 0.3M   exact decimal arithmetic
(= 1 1.0) ;=> false   (== 1 1.0) ;=> true    (= 1 1N) ;=> true
(quot 7 2) (rem -7 2) (mod -7 2)  ;=> 3 -1 1
(with-precision 10 :rounding HALF_UP (/ 1M 3))
```
- By default natural numbers are `long`; an overflowing primitive operation throws `ArithmeticException`. The auto-promoting operators are `+'`, `-'`, `*'`, `inc'` and `dec'`, which promote to BigInt but are less efficient.
- Literals: postfix `N` is BigInt and `M` is BigDecimal. BigInts and floating point types are "contagious": any operation involving a BigInt gives a BigInt, and any involving a double or float gives a double.
- `##NaN` is not `=` or `==` to anything, not even itself; `NaN?` (1.11) tests for it.
- `=` is true only within a numeric category (integer or ratio; floating point; decimal), so `(= 1 1.0)` is false. `==` compares numerically across categories, e.g. `(== 1 1.0 1M)` is true. Categories matter for set elements and map keys too.
- Division `/` of integers that does not reduce to an integer yields a ratio rather than a truncated value; use `quot` for integer division. `mod` truncates toward negative infinity.
- `with-precision` sets the precision and rounding mode for BigDecimal operations; the mode (CEILING, FLOOR, HALF_UP, HALF_DOWN, HALF_EVEN, UP, DOWN, UNNECESSARY) defaults to HALF_UP.
- Money: prefer `BigDecimal` (`M` literals) with explicit rounding, or integer cents.
- While `*unchecked-math*` is true, `+`, `-`, `*`, `inc`, `dec` and the coercions compile without overflow checks (default false); `:warn-on-boxed` also warns on boxed math.
- Clojure 1.11 added `clojure.math`, wrappers for `java.lang.Math` functions.

## Failure modes
- Surprise ArithmeticException on long overflow: use the primed operators when values may grow past a long.
- `(= 1 1.0)` is false and so a set or map keyed by mixed integer and floating point numbers does not unify them.

## Self-check
`(+ 0.1 0.2)` vs `(+ 0.1M 0.2M)`; explain the difference.

## Checked
2026-11-03. Confirmed against the clojure.org Numbers reference, the Equality guide and the clojure.core API page: long default and ArithmeticException on overflow, primed operators, ratio rule, N and M literals and contagion, = categories versus ==, NaN, quot/rem/mod, with-precision modes and default, bigint/bigdec, unchecked-add, *unchecked-math*, clojure.math in 1.11 (changes.md). Removed: the overflow message text, automatic BigInt reading of large literals, Math/round, Math/floor, long truncation, format, Double/isNaN, *warn-on-reflection*, the specific clojure.math function names, and the BigDecimal "Non-terminating decimal expansion" message (not in the pages read).
Method: documentation only; no commands were run.
