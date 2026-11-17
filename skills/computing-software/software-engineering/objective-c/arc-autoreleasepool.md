---
id: computing-software.software-engineering.objective-c.arc-autoreleasepool
name: arc-autoreleasepool
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-arc, arc-autoreleasepool]
level: practitioner
status: docs-checked
description: "Use @autoreleasepool to bound temporary memory in loops and secondary threads and understand when pools drain."
sources:
  - https://clang.llvm.org/docs/AutomaticReferenceCounting.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/MemoryMgmt.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# @autoreleasepool
**Goal:** bound the lifetime of autoreleased temporaries.

```objc
@autoreleasepool {
    // statements
}   // pool state restored here
```
- `@autoreleasepool` is a statement followed by a compound statement. On entry the current autorelease pool state is captured; on normal exit (fallthrough, `return`, `break`) the pool is restored to that state, releasing everything in it.
- If the block exits by an exception the pool is not drained.
- It may be used in non-ARC translation units with equivalent semantics.
- A program that refers to the `NSAutoreleasePool` class is ill-formed under ARC.
- Autorelease pools are tied to the current thread and scope.
- For returned values ARC uses a handoff: `objc_autoreleaseReturnValue` makes a best effort to pass ownership to `objc_retainAutoreleasedReturnValue` in the caller, otherwise the object is autoreleased.

## Gotchas
- Wrap long loops that create many temporaries in an inner `@autoreleasepool`.

## Self-check
Place a pool inside a loop body and confirm temporaries are freed each iteration.

## Checked
2026-11-02. Confirmed against the Clang ARC specification (`@autoreleasepool`, runtime `objc_autoreleaseReturnValue`, thread-and-scope remark). Removed: run loop and GCD pool claims, NSThread advice, "cheaper" claim, Instruments sawtooth and return-inside-pool safety claims (not on the page).
Method: documentation only; no commands were run.
