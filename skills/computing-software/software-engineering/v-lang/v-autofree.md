---
id: computing-software.software-engineering.v-lang.v-autofree
name: v-autofree
category: computing-software
field: software-engineering
product: v-lang
tags: [v-autofree, memory-management, autofree, free, manualfree, v-lang]
level: advanced
status: docs-checked
description: "What V's -autofree does (compiler-inserted free calls), its documented WIP status, the default GC, -manualfree and @[manualfree], and custom free() methods."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autofree

Goal: know what autofree does and when not to trust it.

- V documents 4 ways to manage memory. The default is a minimal tracing GC. The second is autofree, enabled with `-autofree`.
- Autofree has the compiler insert the necessary `free` calls during compilation. The docs say it takes care of most objects (~90-100%) and that the small remaining share is freed via the GC.
- Status per the docs: "Autofree is still WIP. Until it stabilises and becomes the default, please avoid using it." Allocations are handled by the GC until autofree is production ready.
- Autofree can be disabled with `-manualfree`, or per function with `@[manualfree]`. The attribute only makes the -autofree mechanism ignore that function's body; it is not related to the garbage collector.
- Define a `free()` method on a custom type (the docs example marks it `@[unsafe]`) and the compiler statically inserts calls to it at the end of each variable's lifetime, as it does with C's `free()` for C data types.
- Fully manual memory is `-gc none`; arena allocation is `-prealloc` (docs: only suited to short-lived, single-threaded, batch-like programs such as compilers).

Gotchas:
- Treat autofree as experimental; test the exact flags you ship.
- A custom `free()` that directly calls builtin `free(receiver)` gets a shallow heap copy when called explicitly on a named value; fields' allocations are not duplicated.

## Checked

Confirmed against the "Memory management" and "Attributes" sections of doc/docs.md in the vlang/v repository, read 2026-11-08. Removed: `-d trace_autofree`, the unverified "unstable RSS" test and the claim about closures/references confusing the analysis (not in the docs). Dropped docs.vlang.io (JavaScript-rendered) and modules.vlang.io as sources.
Method: docs-only read of cited pages, 2026-11-08
