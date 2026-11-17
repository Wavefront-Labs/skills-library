---
id: computing-software.software-engineering.compiler-construction.compilation-caching
name: compilation-caching
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, ccache-sccache, content-addressed-cache, remote-execution, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Build speed"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compiler caching and distributed builds

Goal: speed builds.
- ccache/sccache hash preprocessed source + flags; remote caches (Bazel) share artefacts.
- Require deterministic compilation; avoid `__DATE__`.
- Verify cache hits and correctness.
Verify: second build is near-instant with identical output.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
