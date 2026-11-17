---
id: computing-software.software-engineering.java.primitive-streams-and-summary-statistics
name: primitive-streams-and-summary-statistics
category: computing-software
field: software-engineering
product: java
tags: [java, java-streams, primitive-streams, intstream, summarystatistics, range, boxed]
level: practitioner
status: docs-checked
description: "Use IntStream to build ranges, compute sum/average/summaryStatistics, convert with mapToInt and boxed(), and avoid the sum overflow and single-use traps."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/IntStream.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/Stream.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/IntSummaryStatistics.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/Collectors.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/String.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Primitive streams and summary statistics

`IntStream` (and the long/double variants) carry primitive values and add numeric terminals such as `sum`, `average` and `summaryStatistics`.

## Create
```java
IntStream.range(0, n);                               // 0 inclusive to n exclusive, step 1
IntStream.rangeClosed(1, 10);                        // 1 to 10 inclusive
IntStream.iterate(1, i -> i <= 100, i -> i * 2);     // seed, hasNext, next; stops when hasNext is false
"héllo".chars();                                     // IntStream of char values (UTF-16 units)
"héllo".codePoints();                                // IntStream of code points; surrogate pairs combined
```

## Convert
```java
list.stream().mapToInt(Order::quantity).sum();       // Stream<T> to IntStream (Order is a placeholder)
intStream.boxed();                                   // Stream<Integer>
intStream.asLongStream();  intStream.asDoubleStream();
intStream.mapToObj(i -> "row" + i);                  // Stream<String>
```
`Stream` also has `mapToLong` and `mapToDouble`.

## Terminal operations
`sum()` (int), `average()` (`OptionalDouble`), `min()` / `max()` (`OptionalInt`), `count()` (long), `summaryStatistics()` (`IntSummaryStatistics`).
```java
IntSummaryStatistics s = orders.stream().mapToInt(Order::quantity).summaryStatistics();
s.getMin(); s.getMax(); s.getAverage(); s.getSum(); s.getCount();
```
As a collector, `Collectors.summarizingInt(Order::quantity)` returns an `IntSummaryStatistics`, and `Collectors.averagingInt` returns a `Double`; both can be used as downstream collectors of `groupingBy`. `IntSummaryStatistics` itself is not thread safe, but `Collectors.summarizingInt()` is safe on a parallel stream.

## Gotchas
- `IntStream.sum()` is equivalent to `reduce(0, Integer::sum)` and returns an `int`; `IntSummaryStatistics` documents that it does not check for overflow of the count or the sum. For large totals use `mapToLong` before summing.
- `average()` on an empty stream returns an empty `OptionalDouble`.
- `chars()` zero-extends `char` values and passes surrogates through uninterpreted; use `codePoints()` for characters outside the BMP.
- A stream should be operated on only once; a reused stream may throw `IllegalStateException`, but the Javadoc says reuse cannot always be detected.

## Verify
`IntStream.rangeClosed(1, 100).sum()` is 5050; `IntStream.empty().average()` is an empty `OptionalDouble`.

## Checked
2026-11-03. Confirmed against the Java SE 21 pages for IntStream, Stream, IntSummaryStatistics, Collectors and String: range/rangeClosed/iterate semantics, boxed/asLongStream/asDoubleStream/mapToObj/mapToInt/mapToLong, sum/average/min/max/count/summaryStatistics return types, the summarizingInt and averagingInt collectors, thread-safety and overflow remarks, chars vs codePoints, single-use rule.
Removed (not in the pages read): Kahan summation and sequential-versus-parallel result claims, ArrayList/LinkedList parallel splitting, the quoted exception message, `Arrays.stream`, and the dev.java source.
Method: documentation only; no commands were run.
