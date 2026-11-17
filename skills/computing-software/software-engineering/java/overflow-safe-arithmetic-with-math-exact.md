---
id: computing-software.software-engineering.java.overflow-safe-arithmetic-with-math-exact
name: overflow-safe-arithmetic-with-math-exact
category: computing-software
field: software-engineering
product: java
tags: [java, java-type-system, integer-overflow, addexact, tointexact, arithmeticexception, floormod]
level: practitioner
status: docs-checked
description: "Detect silent int/long overflow with Math.addExact, multiplyExact, toIntExact and absExact, and use floorMod for non-negative remainders."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Math.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overflow-safe arithmetic with Math.*Exact

**Goal:** make overflow fail loudly instead of returning a wrapped value.

## The exact family (java.lang.Math)
- `addExact`, `subtractExact`, `multiplyExact` (int/int, long/int and long/long), `incrementExact`, `negateExact`, `divideExact`, `floorDivExact`, `ceilDivExact` for int and long: each throws `ArithmeticException` if the result overflows.
- `toIntExact(long)` throws if the value overflows an `int`.
- `absExact(int)` / `absExact(long)` (since Java 15) throw for `Integer.MIN_VALUE` / `Long.MIN_VALUE`.
- `multiplyHigh(long, long)` returns the high 64 bits of a 128-bit product when you need the full width.

```java
long total = 0;
for (long p : prices) total = Math.addExact(total, p);   // throws on overflow
int idx = Math.toIntExact(someLong);                      // throws if it does not fit an int
long bytes = Math.multiplyExact(count, 4);                // long * int overload
```
(`prices`, `someLong`, `count` are placeholders.)

## Traps the Javadoc calls out
- `Math.abs(Integer.MIN_VALUE)` returns `Integer.MIN_VALUE`, which is negative; `absExact` throws instead. The same holds for `Long.MIN_VALUE`.
- `Integer.MIN_VALUE / -1` evaluated directly gives `Integer.MIN_VALUE` with no exception; `divideExact` throws in that case (also when `y` is zero). Likewise for `long`.
- `%` can be negative. `Math.floorMod(x, y)` has the same sign as the divisor or is zero, with `floorDiv(x, y) * y + floorMod(x, y) == x`. Examples from the page: `floorMod(-4, +3) == +2` while `-4 % +3 == -1`. Use it for array or ring-buffer indexes with a positive divisor.

## Gotchas
- Plain `+`, `-`, `*` never throw on overflow; only the `*Exact` methods do. Catch `ArithmeticException` where the failure should be handled.
- For values that can exceed `long`, use `BigInteger` or `BigDecimal` rather than catching overflow.

## Verify
Test boundaries: `Integer.MAX_VALUE`, `Integer.MIN_VALUE`, `Long.MAX_VALUE`; for example expect `ArithmeticException` from `Math.addExact(Integer.MAX_VALUE, 1)` and `Math.absExact(Integer.MIN_VALUE)`.

## Checked
2026-11-03. Confirmed against the Java SE 21 `Math` Javadoc: the exact methods and their overloads, absExact since 15, the `abs(MIN_VALUE)` note, divideExact overflow case, floorMod definition and examples, multiplyHigh.
Removed (not in the page read): JIT intrinsic claim, midpoint formulas, `ArraysSupport.newLength` and `Integer.MAX_VALUE - 8` array-size advice, `Arrays.copyOf` overflow note, the dev.java source, and the BigDecimal-for-money remark.
Method: documentation only; no commands were run.
