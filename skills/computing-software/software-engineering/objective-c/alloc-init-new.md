---
id: computing-software.software-engineering.objective-c.alloc-init-new
name: alloc-init-new
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-initialization, alloc-init-new]
level: intro
status: docs-checked
description: "Create objects with nested alloc/init, class factory methods and new, and always use the object returned by init."
sources:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/WorkingwithObjects/WorkingwithObjects.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# alloc, init and factory methods
**Goal:** the standard two-step creation and its variants.

```objc
NSObject *newObject = [[NSObject alloc] init];             // nest alloc inside init
NSNumber *magicNumber = [[NSNumber alloc] initWithInt:42]; // initializer with an argument
NSNumber *same = [NSNumber numberWithInt:42];              // class factory method
XYZObject *object = [XYZObject new];                       // same as [[XYZObject alloc] init]
```
- `alloc` allocates memory for the properties of the class and of every superclass, and zeroes it. That is not enough to initialize the object, so combine it with `init`.
- `init` may return a different object than `alloc` returned, so nest the calls and keep the result of `init`.
- Never write `NSObject *someObject = [NSObject alloc]; [someObject init];`: if `init` returns another object you are left holding the uninitialized one.
- Class factory methods (`numberWithInt:`) usually call straight through to `alloc` and the matching `init` method; they are conveniences.
- `new` is provided by `NSObject`, need not be overridden, and is effectively `alloc` plus `init` with no arguments.
- Literals such as `@"Hello"`, `@42` and `@(84 / 2)` are an alternative for some classes.

## Gotchas
- Use an initializer with arguments when the object needs required values (an `NSNumber` must be created with its value); `new` cannot pass any.

## Self-check
Search for any `alloc` whose result is not immediately passed to an `init` method.

## Checked
2026-11-03. Confirmed against Apple's Programming with Objective-C, "Working with Objects" (alloc, init returning another object, nested calls, factory methods, new, literals). Removed: ownership-by-naming claims (see retain-release-rules), class-cluster remark, `self = [other retain]`, and the `NS_UNAVAILABLE` self-check (not on the page).
Method: documentation only; no commands were run.
