---
id: computing-software.software-engineering.zig.doc-comments
name: doc-comments
category: computing-software
field: software-engineering
product: zig
tags: [zig, doc-comments, zig-lexical, autodoc, zig-std-docs, femit-docs]
level: intro
status: docs-checked
description: "Write /// and //! documentation comments in Zig, where each is allowed, and generate browsable docs with the compiler."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/doc/langref.html.in
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build/Step/Compile.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Doc comments and container doc comments
**Goal:** document public declarations so tooling and readers see them.

## Forms
```zig
//! Container doc comment: describes the whole file (the file is a struct).
//! Must come first in the file or container.

/// Doc comment: attaches to the declaration that follows.
pub fn add(a: i32, b: i32) i32 {
    // Plain comment: ignored by tooling.
    return a + b;
}
```
- A doc comment starts with exactly three slashes (`///`, not `////`); consecutive ones merge into one multiline comment and document whatever immediately follows.
- A doc comment in an unexpected place (middle of an expression, or just before a non-doc comment) is a compile error, and so is an unattached one.
- Doc comments can be interleaved with normal comments; currently, package documentation merges normal comments with doc comments.
- `//!` documents the current module and is a compile error unless it is at the start of a container, before any expressions.

## Generating docs
In build.zig, `Step.Compile.getEmittedDocs()` returns a `LazyPath` for the generated documentation directory; install it with a step of your choice.

## Gotchas
- In the grammar only a declaration (`doc_comment? pub? Decl`) or container member takes a doc comment; a `test` declaration does not, so use plain `//` there.
- Style guidance: omit what the name already says, and use the word "assume" for invariants whose violation is unchecked illegal behavior.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: the Doc Comments, Top-Level Doc Comments and Doc Comment Guidance sections and the grammar (`TestDecl`, `doc_comment?`) of the language reference; `getEmittedDocs` in Compile.zig. Removed: the `-femit-docs`, `zig std` and `zig ast-check` commands, the block-comment, `pub`-only and `zig fmt` claims.

Method: documentation only; no commands were run.

## Self-check
Add `///` above a `pub const`, then add a trailing `///` with nothing after it and confirm the compiler rejects it.
