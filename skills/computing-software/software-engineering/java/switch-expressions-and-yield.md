---
id: computing-software.software-engineering.java.switch-expressions-and-yield
name: switch-expressions-and-yield
category: computing-software
field: software-engineering
product: java
tags: [java, java-14, switch-expression, yield, enums, exhaustiveness]
level: practitioner
status: docs-checked
description: "Write Java 14+ switch expressions with arrow labels and yield, avoid fall-through bugs, and get compiler-checked exhaustiveness over enums."
sources: ["https://openjdk.org/jeps/361", "https://docs.oracle.com/javase/specs/jls/se21/html/jls-15.html#jls-15.28"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Switch expressions and yield (standard since Java 14)

**Goal:** replace statement switches that assign a value with a total expression.

## Forms
```java
int days = switch (month) {
    case JAN, MAR, MAY, JUL, AUG, OCT, DEC -> 31;
    case APR, JUN, SEP, NOV -> 30;
    case FEB -> isLeap ? 29 : 28;
};                                   // no default needed: all enum constants covered

String label = switch (code) {
    case 200 -> "ok";
    case 404 -> { audit(code); yield "not found"; }   // block needs yield
    default  -> throw new IllegalArgumentException("code " + code);
};
```
Old-style colon labels also work in expressions with `yield value;` but still fall through, so prefer arrows. `audit` and `isLeap` are placeholders for your own code.

## Rules
- A switch expression must be exhaustive: for all possible values there must be a matching label. For an enum that means all constants or `default`; sealed types and `default` also work. For an enum switch expression that covers all known constants the compiler inserts a `default` clause (JEP 361), so recompiling after adding a constant makes the compiler check that every case is handled; avoid your own `default` on enums you control so the compiler flags new cases.
- Arrow labels never fall through; no `break` required.
- `case null` is allowed from Java 21 (pattern switch); see the JLS section on switch expressions.

## Gotchas
- `yield` is a restricted identifier (like `var`): do not call a method named `yield` unqualified.
- If an enum constant is added after compilation (separate compilation), a switch expression without a matching label can fail at run time: JLS 15.28 says a `MatchException` is thrown if no switch label applies to the value, and also mentions `IncompatibleClassChangeError`; read the section for the exact cases.

## Verify
Add an enum constant and confirm each switch expression without `default` fails to compile.

## Checked
2026-11-03. Confirmed against JEP 361 (standard in JDK 14, arrow labels with no fall through, yield as a restricted identifier, exhaustiveness and the inserted default for enums, yield inside blocks) and JLS 15.28 (exhaustiveness, `case null`, MatchException and IncompatibleClassChangeError).
Removed (not confirmed in the pages read): the claims about mixing arrow and colon labels, and about `return`/`break`/`continue` leaving a switch expression, and the `-Xlint:all` instruction.
Method: documentation only; no commands were run.
