---
id: computing-software.software-engineering.java.streams-and-collectors
name: streams-and-collectors
category: computing-software
field: software-engineering
product: java
tags: [java, java-streams, collectors, groupingby, tomap, parallel-streams, lambdas, stream-gather, functional-java]
level: practitioner
status: docs-checked
description: "Use Java Streams well: common collectors (groupingBy, toMap merge), laziness and short-circuiting, side-effect rules, parallel stream pitfalls and when a loop is better."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/package-summary.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/Collectors.html", "https://openjdk.org/jeps/485"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streams and collectors

**Goal:** readable data pipelines without the classic stream bugs (duplicate-key
crashes, hidden side effects, slower "parallel" code).

## Collectors you actually need
```java
Map<Dept, List<Emp>> byDept = emps.stream().collect(groupingBy(Emp::dept));
Map<Dept, Long> counts      = emps.stream().collect(groupingBy(Emp::dept, counting()));
Map<Dept, Double> avgPay    = emps.stream().collect(groupingBy(Emp::dept, averagingDouble(Emp::salary)));
Map<Boolean, List<Emp>> p   = emps.stream().collect(partitioningBy(e -> e.salary() > 100_000));
Map<String, Emp> byEmail    = emps.stream().collect(toMap(Emp::email, identity(), (a, b) -> a));
String csv                  = names.stream().collect(joining(", ", "[", "]"));
List<String> list           = names.stream().filter(...).toList();
```
- `toMap` WITHOUT a merge function throws `IllegalStateException` on duplicate keys and
  NPE on null values. Always decide the merge rule.
- Need sorted keys: `groupingBy(f, TreeMap::new, toList())`.
- `collect(Collectors.toList())` makes no guarantee about the list type or mutability.
  Use `toCollection(ArrayList::new)` if you must mutate.

## Laziness and order
Intermediate ops run only on a terminal op, element by element. `findFirst`,
`limit` short-circuit. `sorted`/`distinct` are stateful barriers that buffer everything.

## Side-effect rule
Lambdas must not mutate shared state (`forEach(list::add)` into an outer list). Use a
collector. Mutation breaks under parallel and hides intent.

## Parallel streams
- Pay off only for large, CPU-bound, easily splittable sources. Measure before using.
- Never for blocking I/O calls; use executors or virtual threads.

## Checked exceptions and debugging
Lambdas cannot throw checked exceptions through `Function`; wrap in a helper or use a
loop. Long chains produce unreadable stack traces; extract named methods.

## When a loop wins
Early `return` from nested logic, multiple accumulators, index-based logic, or hot paths
where boxing (`Stream<Integer>`) costs; use `IntStream`/`mapToInt` or a plain loop.
Java 24 `Stream.gather()` (JEP 485) adds custom intermediate ops like windowing.

## Verify
- [ ] Every `toMap` has a merge function or a documented uniqueness guarantee.
- [ ] No `parallel()` without a benchmark justifying it.

## Checked

- Date: 2026-10-28
- Confirmed in the Java SE 21 Javadoc (stream package summary, Collectors) and JEP 485: toMap duplicate keys throw IllegalStateException, Collectors.toList gives no mutability guarantee, laziness and short-circuiting, Stream.gather finalized in JDK 24.
- Removed: Stream.toList mutability and Java 16 claims, peek remark, ForkJoinPool and LinkedList splitting claims, dead dev.java source.
Method: documentation only; no commands were run.
