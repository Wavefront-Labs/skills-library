---
id: computing-software.software-engineering.java.instanceof-pattern-matching
name: instanceof-pattern-matching
category: computing-software
field: software-engineering
product: java
tags: [java, java-control-flow, instanceof-pattern, pattern-variables, flow-scoping, java-16, equals-implementation]
level: practitioner
status: docs-checked
description: "Use Java 16+ instanceof patterns to drop casts, understand flow scoping of pattern variables, and write short equals methods and guarded conditions."
sources: ["https://openjdk.org/jeps/394", "https://docs.oracle.com/javase/specs/jls/se21/html/jls-15.html#jls-15.20.2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pattern matching for instanceof (final in Java 16, JEP 394)

**Goal:** test and bind in one step, with no manual cast.

```java
if (obj instanceof String s && s.length() > 5) {
    flag = s.contains("jdk");          // s is in scope on the right of && and in the true block
}
if (!(o instanceof Point other)) return false;
return x == other.x && y == other.y;   // other is in scope after the early return
```

## Scope rules (flow scoping)
- "A pattern variable is in scope where it has definitely matched." The right operand of `&&` and the true block are in scope; `obj instanceof String s || s.length() > 5` does not compile, because `s` may not have been assigned.
- After `if (!(o instanceof String s)) throw ...;` the variable is in scope for the following statements, because the throwing statement cannot complete normally, so reaching the next statement means the match succeeded.
- Two separate `if (a instanceof Point p)` and `if (b instanceof Point p)` statements can reuse the name `p`; the variable is not in scope after the first `if`.
- Pattern variables are ordinary local variables apart from scope: they can be assigned to (the restriction that they are implicitly final was lifted when the feature was finalised in 16) and they can shadow a field. In the else branch of `if (o instanceof Point p)` a name `p` refers to the field again.

## Typical use: compact equals
```java
@Override public final boolean equals(Object o) {
    return (o instanceof Point other) && x == other.x && y == other.y;
}
```
(JEP 394's own example; `Point` with fields `x` and `y` is a placeholder.)

## Semantics
- At run time, if the expression is `null` the pattern match is false, so no separate null check is needed (JLS 15.20.2).
- The expression must have a reference type or the null type, and the pattern must be applicable at that type, otherwise a compile-time error occurs.
- In Java 16 (JEP 394) it was a compile-time error to test an expression of type S against a pattern of type T when S is a subtype of T. The Java SE 21 rule for the pattern match operator (JLS 15.20.2) states only the applicability requirement above, so check your target language level for this case.
- Future patterns (record deconstruction, `switch`) build on the same mechanism; see the pattern `switch` skill in this library.

## Verify
Unit-test `equals` against `null`, a different class and an equal instance. Search for `(Type) x` immediately after `instanceof Type` as candidates for conversion.

## Checked
2026-11-03. Confirmed against JEP 394 and JLS SE 21 section 15.20.2: syntax, flow scoping rules and examples, `||` error, reuse of names, non-final pattern variables, field shadowing, equals example, null behaviour, applicability rule, Java 16 subtype error.
Fixed: the earlier text claimed total patterns are "allowed since Java 21 (earlier versions reported an error)" as settled fact; the pages read only show the Java 16 error and that the SE 21 text lists no such rule, so it is stated that way now.
Removed (not in the pages read): the rule that a pattern variable cannot shadow an enclosing local, the generic `List<String>` instanceof claim, the long `else if` ladder advice, `--release 17`, the Money example, and the dev.java source (page unavailable).
Method: documentation only; no commands were run.
