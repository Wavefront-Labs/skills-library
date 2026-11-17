---
id: computing-software.software-engineering.objective-c.block-retain-cycles
name: block-retain-cycles
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-blocks, block-retain-cycles]
level: practitioner
status: docs-checked
description: "Detect the self-capture warning, apply weak-strong dance, and know which framework blocks run once (safe) or are stored."
sources:
  - https://clang.llvm.org/docs/BlockLanguageSpec.html
  - https://clang.llvm.org/docs/AutomaticReferenceCounting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# Block retain cycles
**Goal:** avoid cycles when a stored block references its owner.

```objc
__weak typeof(self) weakSelf = self;
self.onDone = ^{
    typeof(self) strongSelf = weakSelf;
    if (!strongSelf) return;
    [strongSelf finish];
};
```
- Capturing a variable copies it into the block at the moment the block literal is evaluated; an object variable is retained when the block is copied to the heap.
- Inside a block in a method, instance variable references are imported through `self`, which is captured as a const copy; so `_x` also captures `self`.
- A block stored by an object that the block itself retains forms a cycle. Break it with a `__weak` local captured instead of `self`, then read it into a strong local at the top of the block.
- `__weak` on a `__block` variable of object type, without garbage collection, keeps the variable without a retain, so it can dangle if the block outlives the object.

## Gotchas
- A strong local taken from `weakSelf` at the top keeps the object alive for the whole block run; check it for `nil` first.

## Self-check
Add a log to `dealloc`, store the block, release the owner and check the log appears.

## Checked
2026-11-02. Confirmed against the Clang "Language Specification for Blocks" (capture, `self` import, `__weak` `__block`, Block_copy retain) and the Clang ARC specification. Removed: `-Warc-retain-cycles` and its warning text, one-shot API list (`dispatch_async`, `UIView animateWithDuration:`), nil-after-run advice, nested-block rule (not stated).
Method: documentation only; no commands were run.
