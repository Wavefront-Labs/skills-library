---
id: computing-software.software-engineering.objective-c.retain-cycles
name: retain-cycles
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-arc, retain-cycles]
level: practitioner
status: docs-checked
description: "Find and break retain cycles (parent/child, delegate, timer, block) with weak references and explicit teardown."
sources:
  - https://clang.llvm.org/docs/AutomaticReferenceCounting.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/MemoryMgmt.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# Retain cycles
**Goal:** prevent leaks where objects hold each other strongly.

```objc
__weak typeof(self) weakSelf = self;
self.handler = ^{
    typeof(self) strongSelf = weakSelf;
    if (!strongSelf) return;
    [strongSelf refresh];
};
```
- ARC does not provide a cycle collector: users must break cycles manually or with weak or unsafe references (`__weak`, `__unsafe_unretained`).
- Reading a `__weak` object retains it until the end of the current full-expression, so messaging through a weak reference is safe for that expression.
- A block stored by an object it captures forms a cycle through that object (see block-retain-cycles); `self` is captured through ivar access too.
- Taking a strong local from the weak reference at the top of the block keeps the object alive for that run; test it for `nil` first.

## Gotchas
- A `__weak` reference to one container does not break a cycle that runs through other strong paths.

## Self-check
Log in `dealloc`, drop the last external reference and confirm it runs.

## Checked
2026-11-02. Confirmed against the Clang ARC specification (introduction on cycles, `__weak` read semantics) and the Blocks specification (ivar capture through `self`). Removed: NSTimer, view controller, Instruments and Memory Graph claims, parent/child ownership rule, delegate rule (not on the pages).
Method: documentation only; no commands were run.
