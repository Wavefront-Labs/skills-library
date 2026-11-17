---
id: computing-software.software-engineering.java.lambdas-and-functional-interfaces
name: lambdas-and-functional-interfaces
category: computing-software
field: software-engineering
product: java
tags: [java, java-lambdas, functional-interfaces, method-references, effectively-final, java-util-function, modern-java]
level: practitioner
status: docs-checked
description: "Write lambdas and method references idiomatically: java.util.function types, effectively-final capture, custom @FunctionalInterface, composing functions and checked exceptions."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/package-summary.html", "https://docs.oracle.com/javase/specs/jls/se21/html/jls-15.html#jls-15.27"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambdas and functional interfaces

**Goal:** concise behaviour-passing code that stays readable and debuggable.

## The core interfaces (java.util.function)
| Interface | Signature | Example |
|---|---|---|
| `Supplier<T>` | `() -> T` | `() -> new ArrayList<>()` |
| `Consumer<T>` | `T -> void` | `log::info` |
| `Function<T,R>` | `T -> R` | `User::email` |
| `Predicate<T>` | `T -> boolean` | `String::isBlank` |
| `UnaryOperator<T>` / `BinaryOperator<T>` | `T -> T` / `(T,T) -> T` | `Integer::sum` |
| `BiFunction<T,U,R>` | `(T,U) -> R` | |
Primitive specialisations (`IntPredicate`, `ToLongFunction`, `IntUnaryOperator`) avoid boxing in hot code.

## Method references
```java
users.stream().map(User::email)              // unbound instance method
     .filter(allowed::contains)              // bound instance method
     .map(String::toLowerCase)
     .forEach(System.out::println);
Supplier<Map<String, User>> s = HashMap::new; // constructor reference
```
Prefer a method reference when it names the operation; prefer a lambda when the reference
would be cryptic.

## Capture rules
Lambdas can capture only effectively final locals:
```java
int count = 0;
list.forEach(x -> count++);                  // compile error
```
Use a stream reduction (`list.size()`, `.count()`, `.sum()`) instead of mutating captured state;
`AtomicInteger` works but signals the wrong design. `this` inside a lambda is the enclosing
instance (unlike anonymous classes).

## Composition
```java
Predicate<User> active = User::isActive;
Predicate<User> eligible = active.and(u -> u.age() >= 18);
lines.stream().filter(Predicate.not(String::isBlank));     // negation helper
Function<String, String> norm = String::trim;
norm = norm.andThen(String::toLowerCase);
Comparator<User> byName = Comparator.comparing(User::lastName).thenComparing(User::firstName);
```

## Custom functional interfaces
```java
@FunctionalInterface
interface RetryPolicy { Duration nextDelay(int attempt, Throwable last); }
```
`@FunctionalInterface` makes the compiler enforce a single abstract method. Define your own
when the name documents intent better than `BiFunction<Integer, Throwable, Duration>`.

## Checked exceptions
Standard interfaces cannot throw checked exceptions. Options: a custom interface with
`throws`, wrap into `UncheckedIOException` inside the lambda, or extract a method that
handles it. Avoid "sneaky throw" hacks in shared code.

## Gotchas
- Debugging: stack traces show `lambda$main$0`; extract complex lambdas into named methods.
- Lambdas over 3 lines usually read better as methods.
- Serialising lambdas is fragile; avoid.

## Checked
2026-10-28: Confirmed in JLS 15.27 and the java.util.function package page: effectively final capture rule, the functional interface shapes and primitive specialisations. Removed the dev.java source (page is a stub) and a version tag that no fetched page states.
Method: documentation only; no commands were run.

## Verify
- [ ] No lambdas mutating captured state via arrays/atomics in stream pipelines.
- [ ] Hot paths use primitive specialisations where boxing shows up in profiles.
