---
id: computing-software.software-engineering.objective-c.arc-bridging
name: arc-bridging
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-arc, arc-bridging]
level: advanced
status: docs-checked
description: "Use __bridge, __bridge_retained and __bridge_transfer to move ownership between ARC objects and non-retainable pointers."
sources:
  - https://clang.llvm.org/docs/AutomaticReferenceCounting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ARC bridging casts
**Goal:** move ownership correctly between ARC objects and non-retainable pointers.

```objc
CFStringRef cf = (__bridge CFStringRef)nsString;     // no ownership change
void *ctx = (__bridge_retained void *)obj;           // ARC releases its claim; recipient balances the +1
id o = (__bridge_transfer id)ctx;                    // ARC now owns the +1
```
- `(__bridge T) op`: no transfer of ownership, ARC inserts no retain operations.
- `(__bridge_retained T) op`: casts a retainable object pointer to a non-retainable pointer type and hands over a +1; the recipient is responsible for balancing it.
- `(__bridge_transfer T) op`: casts a non-retainable pointer to a retainable object pointer and ARC takes ownership of the +1.

## Gotchas
- Using `__bridge_retained` without a matching release leaks; using the casts only to force an unbalanced retain/release is poor form (the spec says so).

## Self-check
Pair every `__bridge_retained` with a `__bridge_transfer` or a Core Foundation release.
## Checked
2026-11-02. Confirmed against the Clang ARC specification (ownership transfer casts). Removed: CFBridgingRetain/CFBridgingRelease, toll-free bridging, Create/Copy naming rules, the CFStringCreateWithCString sample and the analyzer claim (not on the page).
Method: documentation only; no commands were run.
