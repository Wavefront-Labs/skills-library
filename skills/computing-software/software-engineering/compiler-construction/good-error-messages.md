---
id: computing-software.software-engineering.compiler-construction.good-error-messages
name: good-error-messages
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, error-messages, span-rendering, suggestions, compiler-diagnostics, error-recovery, source-spans, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "User-facing quality"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing error messages

Goal: produce helpful diagnostics.
- Include file:line:col, the source line with a caret/underline, what was expected/found, and a suggested fix.
- Group errors, avoid cascades by marking poisoned nodes.
- Test messages with snapshot tests.
Verify: snapshot tests lock the wording and spans.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
