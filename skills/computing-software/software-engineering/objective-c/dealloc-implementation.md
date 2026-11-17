---
id: computing-software.software-engineering.objective-c.dealloc-implementation
name: dealloc-implementation
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-mrc, dealloc-implementation]
level: practitioner
status: docs-checked
description: "Write dealloc correctly: release owned ivars in MRC, call super dealloc last, remove observers, and avoid accessors and weak resurrection."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/Articles/MemoryMgmt.html
  - https://clang.llvm.org/docs/AutomaticReferenceCounting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# dealloc
**Goal:** clean up resources without breaking invariants.

```objc
- (void)dealloc {
    if (_fd >= 0) close(_fd);     // non-retainable resource
    // no [super dealloc] under ARC
}
```
- Under ARC a program that sends `dealloc` or uses `@selector(dealloc)` is ill-formed; never call it directly.
- A class may define `dealloc`. It runs after the final release but before the object is deallocated or its instance variables are destroyed; the superclass `dealloc` is called automatically when it returns.
- Legitimate uses include freeing non-retainable resources. Failing to call `[super dealloc]` in a non-ARC implementation is nearly always a bug.
- ARC destroys instance variables at some point after control enters the root class `dealloc`; the order is unspecified, within a class and between sub- and superclasses.
- Sending messages from `dealloc` is generally discouraged: a subclass may rely on invariants broken during `dealloc`.
- If an instance variable's strong object has side effects on destruction that must be ordered, clear the variable manually in `dealloc`, or move the side effects into a separate teardown phase.

## Gotchas
- Do not rely on the order in which ARC releases instance variables.

## Self-check
Review every `dealloc` for message sends and for ordering assumptions between instance variables.

## Checked
2026-11-02. Confirmed against the Clang ARC specification (`dealloc` special method section): ill-formed sends, timing, automatic superclass call, ivar destruction order, message-send caution, manual clearing. Removed: NSNotificationCenter observer and iOS 9 / macOS 10.11 claims, property accessor and KVO advice, scarce-resource and exception remarks, MRC example (not on the page).
Method: documentation only; no commands were run.
