---
id: computing-software.software-engineering.groovy.groovy-idioms
name: groovy-idioms
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, groovy-idioms, groovy-style]
level: practitioner
status: docs-checked
description: "Style guide rules: omit semicolons/return/public, use def vs types, GString only when interpolating, safe navigation, closures, and named args."
sources:
  - https://groovy-lang.org/style-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Idiomatic Groovy style
- No semicolons; `return` of the last expression is optional (often omitted in short methods and closures, but use it or a blank line when it reads better). With `def` methods the last expression may surprise you (`m2.c = 3` returns 3), so prefer a concrete return type such as `void` or a type.
- Omit `public` (classes and methods are public by default); use `@PackageScope` for package-private. Omit getters/setters for plain properties: a field with no visibility modifier generates a private field plus getter and setter, and your own accessor replaces the generated one.
- Use either `def` or a type, never both (`def String name`). Omit `def` on constructors and untyped parameters.
- Prefer `==` over `equals`: it avoids `NullPointerException`; use `a.is(b)` for reference identity.
- Use `?:` (Elvis) for defaults and `?.` for null-safe navigation.
- Prefer single quotes for plain strings and double quotes only when interpolating; use slashy strings (`/fo+\/ba+r/`) for regexes so backslashes need no doubling. `"${-> i}"` evaluates lazily.
- Named parameters with the default constructor (`new Server(name: 'Obelix')`) call the constructor, then the setters in order.
- `with {}` repeats a receiver (returns the closure's last value); `tap {}` returns the object itself.
- Prefer the closure-after-parentheses form (`list.each { println it }`). Parentheses are still required for nested calls and for calling a no-arg method (`bar()`; `def m = bar` fails).
- Use native syntax for lists `[]`, maps `[k: v]`, ranges `10..20` and `10..<20`, and the `in` and `<<` operators.
- Groovy truth: null, empty and zero are false, so `if (name)` replaces explicit null and length checks.
- `assert` is always checked in Groovy (no activation flag).
- Strongly type public APIs (parameters and return types); `def` is fine for private code where the type is obvious.
- `catch (any)` with no type catches `Exception`, not `Throwable`.

## Gotchas
- Optional-everything style can hurt readability: keep parentheses where omitting them stops working or obscures the call.

## Self-check
Refactor a Java-style class using the list above and confirm tests still pass.

## Checked

Checked 2026-11-09 against groovy-lang.org/style-guide.html, read in full (sections 1 to 21).
Confirmed: every rule above, including the `def` return-value warning, `@PackageScope`, `with`/`tap`, eager versus lazy GString evaluation, parentheses requirements, and `catch (any)`.
Removed as unconfirmed: `var` for locals, `@CompileStatic` for library code, `list*.prop`, and the note on `with` resolving outer variables.

Method: documentation only; no commands were run.
