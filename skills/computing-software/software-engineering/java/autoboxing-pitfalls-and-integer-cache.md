---
id: computing-software.software-engineering.java.autoboxing-pitfalls-and-integer-cache
name: autoboxing-pitfalls-and-integer-cache
category: computing-software
field: software-engineering
product: java
tags: [java, java-type-system, autoboxing-pitfalls, integer-cache, wrapper-types, nullpointerexception, boxed-comparison]
level: practitioner
status: docs-checked
description: "Avoid autoboxing bugs: == on Integer, NPE on unboxing null, accidental boxing in hot loops, and the overload trap of List.remove(int) vs remove(Object)."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Integer.html", "https://docs.oracle.com/javase/specs/jls/se21/html/jls-5.html#jls-5.1.7", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/List.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autoboxing pitfalls and the Integer cache

**Goal:** know the ways boxing breaks working code and the fix for each.

## 1. `==` on wrappers compares references
`Integer.valueOf` always caches values in -128..127 inclusive and may cache others (JLS 5.1.7 guarantees identity for boxed `true`, `false`, chars up to `\u007f` and ints in -128..127), so:
```java
Integer a = 127, b = 127;  a == b   // true
Integer c = 128, d = 128;  c == d   // not guaranteed; false on a default JVM
```
Fix: `a.equals(b)`, `Objects.equals(a, b)`, or unbox one side (`a.intValue() == b`).
The `Integer(int)` constructor is deprecated for removal; use `Integer.valueOf`.

## 2. Unboxing null throws NullPointerException
The JLS says unboxing conversion of a null reference throws `NullPointerException`:
```java
Map<String,Integer> counts = ...;
int n = counts.get("missing");   // NPE
int n2 = counts.getOrDefault("missing", 0);   // fix
```
The same applies to any mix of primitive and wrapper where the wrapper is unboxed (assignment, arithmetic, method arguments).

## 3. Hidden allocation in hot paths
`Long sum = 0L; for (...) sum += x;` unboxes and reboxes on every iteration, which can allocate a new `Long`. Use primitive `long`, `LongStream`, or primitive-specialised collections. Measure before and after.

## 4. Overload resolution
`List<Integer>` has both `remove(int index)` and `remove(Object)`: `l.remove(1)` removes the element at index 1; `l.remove(Integer.valueOf(1))` removes the value 1.

## Verify
Add a unit test with values 127 and 128 for any equality helper, and review code for `==` between two wrapper operands.

## Checked
Checked 2026-11-08 against the Integer API page (Java 21: `valueOf` caches -128 to 127 and may cache more; constructor deprecated for removal) and JLS 5.1.7 (boxing identity guarantee; unboxing null throws NullPointerException).
Removed as unconfirmed in those pages: the `-XX:AutoBoxCacheMax` option, the ternary NPE example, Double.equals NaN/-0.0 behaviour, Short/Byte compound assignment note, the SpotBugs rule name and the JFR advice. The `remove(int index)` and `remove(Object o)` overloads and `Map.getOrDefault` were confirmed in the List and Map API pages.
Method: documentation only; no commands were run.
