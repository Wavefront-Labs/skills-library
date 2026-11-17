---
id: computing-software.software-engineering.java.var-local-variable-type-inference
name: var-local-variable-type-inference
category: computing-software
field: software-engineering
product: java
tags: [java, java-10, var, type-inference, lvti, style]
level: practitioner
status: docs-checked
description: "Use var for local variables only where the right-hand side makes the type obvious; know where var is banned and the traps with diamond, literals and lambdas."
sources: ["https://openjdk.org/projects/amber/guides/lvti-style-guide", "https://openjdk.org/jeps/286", "https://openjdk.org/jeps/323"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# var and local variable type inference (JEP 286, Java 10+)

**Goal:** cut noise without hiding types from the reader.

## Where it is legal
Local variables with an initializer, including `for` and enhanced-`for` variables and try-with-resources variables, and (JEP 323, Java 11) lambda parameters written as `(var x, var y) -> x.process(y)`, whose purpose is to let you add annotations to implicitly typed parameters. `var` is a reserved type name, not a keyword.

```java
var users = new ArrayList<User>();          // good: type is on the right
var n = 0L;                                  // long, not int
for (var e : map.entrySet()) { ... }
```

## Style rules (OpenJDK LVTI style guide)
1. Reading code is more important than writing code; code should be clear from local reasoning and should not depend on IDE type hints.
2. Use `var` when the initializer shows the type (`new`, a cast, a literal) or when the type is a long name that adds nothing.
3. Do not use it when the method name hides the type, as in `var result = service.process();`.
4. Prefer good variable names; with numeric literals take care that `int` vs `long`/`double` is what you mean (the guide shows `long base = 17;` being narrowed or widened silently with an explicit type).
5. With diamond or generic methods, make sure the constructor or method arguments provide the type information, because the inferred type may change when `var` is used.

## Gotchas
- `var x;`, `var x = null;`, lambdas, method references and array initializers (`var f = () -> 1;`, `var a = {1,2};`) are compile errors because there is no type to infer.
- Diamond with no target type falls back to `Object`: `var list = new ArrayList<>();` is an `ArrayList<Object>`. Write the type argument.
- Non-denotable types can be inferred, including anonymous class types and intersection types; an anonymous class's members stay usable via `var`.
- Not allowed for fields, method parameters or return types.

## Verify
Reviewing: every `var` line should be readable without an IDE type hint; if not, spell the type.

## Checked
2026-11-03. Confirmed against the OpenJDK LVTI style guide, JEP 286 and JEP 323: legal positions, errors for null/lambda/method reference/array initializer, non-denotable types, diamond fallback, numeric literal advice, lambda-parameter form and its purpose.
Removed (not in the pages read): the `javac --release 21` instruction, the ternary claim, and `var` used as an ordinary variable name.
Method: documentation only; no commands were run.
