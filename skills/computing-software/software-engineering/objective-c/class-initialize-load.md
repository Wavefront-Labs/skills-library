---
id: computing-software.software-engineering.objective-c.class-initialize-load
name: class-initialize-load
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-initialization, class-initialize-load]
level: advanced
status: docs-checked
description: "Know when +initialize runs, why subclasses trigger the superclass implementation, and guard it with a class check."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocObjectsClasses.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# +initialize
**Goal:** know exactly when the class-level initialization hook runs.

- If a class uses static or global variables, `initialize` is a good place to set their initial values; you do not need to write it if no initialization is required.
- The runtime sends `initialize` to every class object before the class receives any other message, and after its superclass has received `initialize`.
- If a subclass does not implement `initialize`, the message is forwarded to the superclass, so the superclass implementation runs again for the subclass. Class A must therefore ensure its logic runs only once, and for the appropriate class.
```objc
+ (void)initialize
{
    if (self == [ThisClass class]) {
        // Perform initialization here.
    }
}
```
- The runtime sends `initialize` to each class individually, so do not send `initialize` to the superclass from inside your implementation.

## Self-check
Log `NSStringFromClass(self)` in `+initialize` of a base class with two subclasses that do not implement it and confirm the guard is needed.

## Checked
2026-11-08. Confirmed against the archived "Objective-C Programming Language" chapter on objects, classes and messaging (Initializing a Class Object): timing, subclass forwarding, the `self == [ThisClass class]` template, no superclass send. Removed: all `+load` claims (timing, ordering, categories, swizzling, launch cost), `dispatch_once` advice, thread-blocking and locking gotchas; the Runtime Guide source was not used. The page is a retired document.
Method: documentation only; no commands were run.
