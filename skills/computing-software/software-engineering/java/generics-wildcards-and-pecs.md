---
id: computing-software.software-engineering.java.generics-wildcards-and-pecs
name: generics-wildcards-and-pecs
category: computing-software
field: software-engineering
product: java
tags: [java, java-generics, pecs, wildcards, bounded-types, type-erasure, unchecked-warnings, heap-pollution, safevarargs]
level: advanced
status: docs-checked
description: "Write Java generic APIs correctly: bounded type parameters, ? extends / ? super (PECS), type erasure consequences, and fixing unchecked warnings."
sources: ["https://docs.oracle.com/javase/tutorial/java/generics/wildcardGuidelines.html", "https://docs.oracle.com/javase/specs/jls/se21/html/jls-4.html#jls-4.6"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generics, wildcards and PECS

**Goal:** generic method signatures that accept every type they safely can, and no
`ClassCastException` hiding behind ignored warnings.

## PECS: Producer Extends, Consumer Super
```java
static <T> void copy(List<? super T> dest, List<? extends T> src) {
    for (T t : src) dest.add(t);
}
static double sum(Collection<? extends Number> xs) { ... }   // reads Numbers: producer
static void fill(List<? super Integer> out) { out.add(1); }  // writes Integers: consumer
```
- `List<Integer>` is NOT a `List<Number>` (invariance). `? extends Number` lets callers
  pass either.
- From `? extends T` you can read `T` but not add (except null). Into `? super T` you
  can add `T` but read only `Object`.
- Return types should NOT use wildcards; it pushes them onto callers.
- `Comparator<? super T>` is the standard shape (`Collections.sort`, `stream.sorted`).

## Bounded type parameters
```java
static <T extends Comparable<? super T>> T max(Collection<? extends T> xs)
```
Use a named type parameter when it appears more than once (ties argument to return);
otherwise a wildcard is simpler.

## Type erasure consequences
- No `new T()`, `new T[]`, `instanceof List<String>`, or overloads differing only in type
  arguments. Pass `Class<T>` (or a `Supplier<T>`) when you need runtime type.
- Primitives require boxing: `List<int>` impossible; consider `IntStream` or primitive
  collections for hot paths.

## Unchecked warnings
- Never suppress globally. Put `@SuppressWarnings("unchecked")` on the smallest
  declaration with a comment explaining why the cast is safe.
- Generic varargs (`List<String>...`) create heap pollution; annotate safe methods with
  `@SafeVarargs` (only on static, final or private methods and constructors) and never store or expose the array.
- Raw types (`List` without `<>`) disable checking; compile with javac lint enabled for unchecked and rawtypes warnings.

## Checked
2026-10-28: Confirmed in the Oracle wildcard guidelines tutorial and JLS 4: PECS style guidance, unchecked warnings from generic varargs, SafeVarargs restricted to methods that are neither overridable (static, final or private). Removed the dev.java source (stub), the Jackson super-type-token claim and the exact javac flag combination (javac man page not fetched).
Method: documentation only; no commands were run.

## Verify
- [ ] javac reports no unchecked or rawtypes warnings (or each is justified).
- [ ] Public APIs accept `Collection<? extends T>` / `Consumer<? super T>` where they only read/write.
