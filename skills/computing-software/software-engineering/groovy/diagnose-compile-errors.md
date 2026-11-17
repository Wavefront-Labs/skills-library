---
id: computing-software.software-engineering.groovy.diagnose-compile-errors
name: diagnose-compile-errors
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, diagnose-compile-errors]
level: practitioner
status: draft
description: "Interpret MissingMethodException, unable to resolve class, and compile phase messages, and enable debug options."
sources:
  - https://groovy-lang.org/semantics.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading compile and runtime errors
- `MissingMethodException: No signature of method X.m() is applicable for argument types: (...)` lists candidate signatures; check the argument runtime types.
- `unable to resolve class` means a missing import or dependency (add `@Grab` or classpath).
- `Script1.groovy: 3: expecting '}'` reports line/column in the script: with Gradle, the real file path is shown.
- Full stack traces: Groovy filters its internals; use the full-stack-trace system property to see all frames (name unconfirmed; see `StackTraceUtils`).
- Java version mismatch: `Unsupported class file major version` means Groovy too old for the running JDK.

## Gotchas
- Groovy version and JDK compatibility matrix is on the download page; check before upgrading the JDK.
- Do not catch and ignore `Throwable` in scripts.

## Self-check
Cause a MissingMethodException and read the candidate signature list.
