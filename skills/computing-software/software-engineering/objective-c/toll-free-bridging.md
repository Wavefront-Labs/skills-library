---
id: computing-software.software-engineering.objective-c.toll-free-bridging
name: toll-free-bridging
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-c-interop, toll-free-bridging]
level: advanced
status: docs-checked
description: "Convert between Foundation and Core Foundation types, and follow the Create/Copy/Get memory rules with ARC bridge casts."
sources:
  - https://developer.apple.com/documentation/foundation
  - https://clang.llvm.org/docs/AutomaticReferenceCounting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# Toll-free bridging
**Goal:** move between Core Foundation and Objective-C pointers without leaks.

```objc
CFArrayRef arr = (__bridge CFArrayRef)nsArray;      // no ownership change
void *ctx = (__bridge_retained void *)obj;           // +1 handed to the recipient
id o = (__bridge_transfer id)ctx;                    // ARC takes ownership of the +1
```
- ARC does not manage pointers of Core Foundation type; `CFRetain` and `CFRelease` remain the programmer's job.
- `(__bridge T) op`: no ownership transfer, ARC inserts no retain operations.
- `(__bridge_retained T) op`: retainable object pointer to non-retainable pointer, handing over a +1 the recipient must balance.
- `(__bridge_transfer T) op`: non-retainable pointer to retainable object pointer; ARC takes ownership of the +1.
- Using the casts only to force an unbalanced retain or release is poor form.

## Gotchas
- A `__bridge_retained` without a matching release leaks.

## Self-check
Pair each `__bridge_retained` with a `__bridge_transfer` or a Core Foundation release.

## Checked
2026-11-02. Confirmed against the Clang ARC specification (ownership transfer casts, Core Foundation not managed). Removed: toll-free pair list, Create/Copy/Get naming rule, CFBridgingRetain/CFBridgingRelease, CF_RETURNS_RETAINED and CF_IMPLICIT_BRIDGING_ENABLED, CGImageRef remark, analyzer and Instruments checks (not on the page).
Method: documentation only; no commands were run.
