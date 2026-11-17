---
id: computing-software.software-engineering.objective-c.kindof-types
name: kindof-types
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-generics, kindof-types]
level: advanced
status: gated
description: "Use __kindof to let subclass messages work on collection elements and returns without casts while keeping type safety."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Introduction/introObjectiveC.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# __kindof
**Goal:** return or hold "this class or any subclass" types.

```objc
@property (nonatomic, readonly) NSArray<__kindof UIView *> *subviews;
UIButton *b = view.subviews.firstObject;      // no cast warning under __kindof
- (__kindof ABCShape *)shapeAtIndex:(NSUInteger)i;
```
- `__kindof T *` means T or a subclass of T. Assigning it to a subclass-typed variable is allowed without a cast; plain `T *` to a subclass variable warns. (gated: unconfirmed, source is paywalled or blocked)
- Typical use: containers and accessors returning supertype but frequently used as a subtype.
- It keeps messages specific to subclasses available when the static type is the kindof type.
- Swift imports it as the base type (the subclass relationship is dropped).
- Syntax placement: before the class name inside generic arguments or as the return type.

## Gotchas
- It weakens checking; overuse hides bugs.
- Not meaningful on `id` (just use `id`).

## Self-check
Assign an element of `NSArray<__kindof UIView *>` to `UIButton *` and confirm no warning, then do it with `NSArray<UIView *>` and confirm the warning.

## Checked
2026-11-02. Not confirmed: the Apple Objective-C guide landing page does not state the `__kindof` rules. Claims left in place are unchecked; the first bullet carries the gate marker.
Method: documentation only; no commands were run.
