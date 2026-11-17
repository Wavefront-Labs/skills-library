---
id: computing-software.software-engineering.groovy.exception-handling
name: exception-handling
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, exception-handling, groovy-errors]
level: practitioner
status: docs-checked
description: "Exception handling in Groovy: unchecked treatment of checked exceptions, multi-catch, try-with-resources, withCloseable, and common runtime exceptions."
sources:
  - https://groovy-lang.org/semantics.html
  - https://groovy-lang.org/objectorientation.html
  - https://groovy-lang.org/differences.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exception handling in Groovy
- Groovy treats checked exceptions like unchecked ones: you need not declare or catch them. You may still declare them with `throws`; the declaration is then part of the method in bytecode, which matters for Java callers.
- Multi-catch works: `catch ( IOException | NullPointerException e ) { }` (since Groovy 2.0).
- Java-style `try (...)` with resources is supported, including the Java 9 form that reuses an existing variable; Groovy also offers `withCloseable` on closeable objects as an alternative.
- Calling a method that does not exist raises `MissingMethodException`; a failed cast raises `GroovyCastException`.

## Checked

2026-11-03. Confirmed against the Semantics chapter (multi-catch, ARM try with resources, `withCloseable`), the Object orientation chapter (exception declaration) and the Differences with Java page (`MissingMethodException`, `GroovyCastException`). Removed: the stack-trace sanitizing note, `PowerAssertionError` and `ReadOnlyPropertyException`, the `InvokerInvocationException` note, the claim about what `catch (e)` catches, and the code snippet and self-check.

Method: documentation only; no commands were run.
