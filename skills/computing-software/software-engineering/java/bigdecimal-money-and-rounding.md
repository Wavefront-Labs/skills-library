---
id: computing-software.software-engineering.java.bigdecimal-money-and-rounding
name: bigdecimal-money-and-rounding
category: computing-software
field: software-engineering
product: java
tags: [java, java-type-system, bigdecimal-rounding, bigdecimal, money, roundingmode, mathcontext, floating-point]
level: practitioner
status: docs-checked
description: "Handle money and decimals in Java with BigDecimal: construct from strings, set scale with RoundingMode, divide safely, compare with compareTo, avoid double."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/math/BigDecimal.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/math/RoundingMode.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BigDecimal for money and rounding

**Goal:** exact decimal arithmetic with explicit rounding rules.

## Construct correctly
```java
new BigDecimal("0.1");          // exact decimal value
BigDecimal.valueOf(0.1);        // uses Double.toString(double), so it gives 0.1
new BigDecimal(0.1);            // exact value of the binary double, not 0.1 (do not)
```
The Javadoc calls `valueOf(double)` the generally preferred way to convert a double, because the `BigDecimal(double)` constructor is unpredictable in that sense.

## Scale and rounding
```java
BigDecimal price = new BigDecimal("19.995");
price.setScale(2, RoundingMode.HALF_EVEN);   // 20.00 (tie goes to the even neighbour)
a.divide(b);                                  // ArithmeticException if the quotient is non-terminating
a.divide(b, 4, RoundingMode.HALF_UP);         // fixed scale
a.divide(b, new MathContext(10, RoundingMode.HALF_EVEN)); // fixed precision
```
`HALF_UP` is "commonly taught at school"; `HALF_EVEN` is sometimes known as "Banker's rounding" and statistically minimises cumulative error over a sequence of calculations (RoundingMode Javadoc). Pick the mode from the business rule the money domain requires. Round once at the end of a calculation, not at each step, unless the rule says per line.

## Comparing
- `equals` considers scale: `2.0` is not equal to `2.00` by `equals` (unscaled values 20 and 200). Use `compareTo(...) == 0`; `compareTo` treats values that differ only in scale as equal.
- `hashCode` is computed from the unscaled value and the scale, so do not use raw BigDecimals as HashMap keys; normalise with `stripTrailingZeros()` first (a numerically zero value returns `BigDecimal.ZERO`).
- `toString()` uses scientific notation when an exponent is needed; use `toPlainString()` for display.

## Gotchas
- Add and subtract: result scale is `max` of the operand scales; multiply: scale is the sum of the operand scales.
- Keep the database column and any JSON mapping decimal as well, never double; check how your driver and JSON library map the type.

## Verify
Test that adding `1.10` and `2.20` as BigDecimals gives scale 2 and compares equal to `3.30`, and that a 3-way split of `100.00` allocates the leftover cent explicitly.

## Checked
Confirmed on the cited BigDecimal and RoundingMode Javadoc (Java 21): valueOf via Double.toString, constructor behaviour, divide ArithmeticException, scale rules for add/subtract/multiply, equals vs compareTo, hashCode inputs, stripTrailingZeros zero case, toString scientific notation, HALF_UP/HALF_EVEN descriptions. Removed: DECIMAL64 "16 digits", "since Java 8", tax/accounting practice claims, NUMERIC(19,4), and the Jackson feature name (no cited page covers them).
Method: docs-only read of cited pages, 2026-11-08
