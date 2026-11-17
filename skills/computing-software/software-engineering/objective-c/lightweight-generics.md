---
id: computing-software.software-engineering.objective-c.lightweight-generics
name: lightweight-generics
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-generics, lightweight-generics]
level: practitioner
status: gated
description: "Declare and use lightweight generics like NSArray<NSString *> *, create generic classes with type parameters and variance."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Introduction/introObjectiveC.html
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lightweight generics
**Goal:** express element types for compile-time checking.

```objc
NSArray<NSString *> *names = @[@"a"];
NSDictionary<NSString *, NSNumber *> *scores;
@interface ABCBox<__covariant ObjectType> : NSObject
- (instancetype)initWithItem:(ObjectType)item;
@property (nonatomic, readonly) ObjectType item;
@end
ABCBox<NSString *> *b = [[ABCBox alloc] initWithItem:@"x"];
```
- Generics are compile-time only; they are erased at runtime, so nothing is checked on insertion at runtime. (gated: unconfirmed, source is paywalled or blocked)
- Variance: `__covariant` allows `Box<NSString *>` where `Box<NSObject *>` expected; `__contravariant` the reverse; default invariant.
- Bounded: `<ObjectType : id<NSCopying>>` or `<T : NSObject *>`.
- Unspecialized use (`NSArray *`) is treated as `NSArray<id> *`.
- Swift imports these as typed generics, which is the main payoff.

## Gotchas
- Mismatch yields warnings ("incompatible pointer types"), not errors; use `-Werror` selectively.
- You can still put wrong types in via `id` or KVC.

## Self-check
Add a wrong-type element to `NSMutableArray<NSString *>` via a typed variable and confirm a warning.

## Checked
2026-11-02. Not confirmed: the Apple Objective-C guide landing page does not state the generics and variance rules. Claims left in place are unchecked; the first bullet carries the gate marker.
Method: documentation only; no commands were run.
