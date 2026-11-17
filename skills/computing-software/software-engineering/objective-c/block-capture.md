---
id: computing-software.software-engineering.objective-c.block-capture
name: block-capture
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-blocks, block-capture]
level: practitioner
status: docs-checked
description: "Understand how blocks capture variables by value, use __block for mutable captures, and how object captures retain."
sources:
  - https://clang.llvm.org/docs/BlockLanguageSpec.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Block variable capture
**Goal:** know what a block sees and can change.

```objc
int x = 1;
void (^b)(void) = ^{ NSLog(@"%d", x); };   // captured as a const copy when the block literal is evaluated
x = 2; b();                                 // prints 1
```
- Variables referenced in a block are imported and captured as `const` copies; the capture is performed at the time the block literal expression is evaluated.
- To modify a captured variable declare it `__block`; such variables are shared with the block rather than copied.
- A block starts on the stack; the runtime function `Block_copy` copies it to the heap.

## Gotchas
- Mutating an unqualified captured variable is a compile error.

## Self-check
Write the print above and confirm it prints 1.
## Checked
2026-11-02. Confirmed against the Clang "Language Specification for Blocks" and the Clang ARC specification (Block_copy): const-copy capture at literal evaluation. Removed: ARC retain details for captured objects, `__block` counter example, cycle-breaking advice, global/static capture and stack-array claims.
Method: documentation only; no commands were run.
