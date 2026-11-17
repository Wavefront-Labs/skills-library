---
id: computing-software.software-engineering.compiler-construction.strings-and-unicode
name: strings-and-unicode
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, utf8-representation, grapheme-clusters, string-interning, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Text handling"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Strings and Unicode

Goal: implement strings soundly.
- Choose UTF-8 (byte-indexed) or UTF-16; distinguish code points from grapheme clusters; normalise (NFC) for comparison; validate input.
- Intern identifiers and short strings for fast equality.
- Rope or builder types for concatenation.
Verify: emoji and combining-mark tests behave as documented.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
