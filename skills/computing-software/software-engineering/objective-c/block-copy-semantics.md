---
id: computing-software.software-engineering.objective-c.block-copy-semantics
name: block-copy-semantics
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-blocks, block-copy-semantics]
level: advanced
status: docs-checked
description: "Know stack vs heap blocks, when to copy under MRC, and why block properties use copy while ARC copies automatically."
sources:
  - https://clang.llvm.org/docs/BlockLanguageSpec.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/MemoryMgmt.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# Block copy semantics
**Goal:** keep blocks valid after the creating scope ends.

- A block that captures values starts on the stack. The runtime function `Block_copy` copies it to the heap (reference count 1), or, if it is already on the heap, increments its reference count. `Block_release` decrements and destroys the heap block at zero.
- Under ARC, whenever the semantics call for retaining a block-pointer value the effect is a `Block_copy`; the optimizer may remove copies it can prove unnecessary. Converting a block pointer to a non-block pointer type such as `id` also calls `Block_copy`, and a block passed as a variadic argument is implicitly converted to `id`.
- Blocks are Objective-C objects; as properties they follow the assign, retain and copy attribute logic, and Foundation supplies `-copy` and `-release` for them.
- `Block_copy` retains the objects held in captured automatic variables.
- A `__block` variable may start on the stack and is moved to the heap by `Block_copy` of a referencing block.
```objc
@property (nonatomic, copy) void (^handler)(void);
```

## Gotchas
- Without ARC, a stack block that outlives its scope without a copy refers to dead stack storage.
- It is a runtime error to assign a stack-based block into `__weak` storage.

## Self-check
List each place a block is stored beyond its creating scope and check it is copied (or ARC does it).

## Checked
2026-11-02. Confirmed against the Clang "Language Specification for Blocks" and the Clang ARC specification (introduction, block pointer retains): stack-to-heap `Block_copy`, `Block_release`, ARC copy rule, `id` conversion, `__block` migration, `__weak` error, Foundation `-copy`/`-release`. Removed: global-block no-op claim, `<Block.h>`, `qsort_b`, GCD copy remarks, `NSStackBlock` note and the crash self-check (not on those pages).
Method: documentation only; no commands were run.
