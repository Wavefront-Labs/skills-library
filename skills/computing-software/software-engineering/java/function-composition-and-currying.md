---
id: computing-software.software-engineering.java.function-composition-and-currying
name: function-composition-and-currying
category: computing-software
field: software-engineering
product: java
tags: [java, java-interfaces, function-composition, andthen, compose, currying, predicate-combinators, comparator-chaining]
level: practitioner
status: docs-checked
description: "Compose Java functions with andThen/compose, Predicate and/or/negate, Comparator.thenComparing, and curry by returning Function<A, Function<B, C>>."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/Function.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/Predicate.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Comparator.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Function composition and currying

## Function
```java
Function<String,String> trim = String::trim;
Function<String,Integer> len = String::length;
Function<String,Integer> trimmedLen = trim.andThen(len);   // trim first, then len
Function<String,Integer> same       = len.compose(trim);   // identical: compose runs the argument first
Function.<String>identity();
```
`f.andThen(after)` applies `f` then `after`; `f.compose(before)` applies `before` then `f`. An exception from either function is relayed to the caller of the composed function.

## Predicate
```java
Predicate<User> active = User::isActive;
Predicate<User> admin = u -> u.role() == ADMIN;
var target = active.and(admin.negate()).or(Predicate.not(User::isBanned));
Predicate.isEqual("x");
```
`and` and `or` short-circuit: if this predicate is false (for `and`) or true (for `or`), the other is not evaluated. `Predicate.not(target)` returns the negation of the supplied predicate (it calls `target.negate()`), so `Predicate.not(String::isBlank)` replaces `s -> !s.isBlank()` in streams.

## Comparator chains
```java
Comparator<Person> byName = Comparator.comparing(Person::lastName)
    .thenComparing(Person::firstName)
    .thenComparingInt(Person::age)
    .reversed();
Comparator.nullsFirst(Comparator.naturalOrder());
```

## Currying
Java has no automatic currying; return functions:
```java
Function<Integer, Function<Integer,Integer>> add = a -> b -> a + b;
Function<Integer,Integer> plus5 = add.apply(5);
```

## Gotchas
- `reversed()` reverses the whole comparator it is called on, so place it last in the chain, or reverse one inner comparator via `Comparator.comparing(f, Comparator.reverseOrder())`.

## Verify
Unit test the composed function on empty inputs; assert comparator `sort` order against a literal expected list.

## Checked
2026-11-09. Confirmed against the Java 21 Function, Predicate and Comparator API pages: andThen/compose ordering and exception relay, identity, and/or short-circuiting, negate, not, isEqual, comparing, thenComparing, thenComparingInt, reversed, nullsFirst, naturalOrder, reverseOrder (names present on the Comparator page).
Removed: the "BiFunction has andThen only" and "Java 11+" notes, the type-inference warning, the stack-frame remark and the advice for more than two arguments (not on the cited pages); dev.java/learn/lambdas was dropped as a source (no content returned).
Method: documentation only; no commands were run.
